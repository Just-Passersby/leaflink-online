import math
import re
from typing import Annotated

from fastapi import APIRouter, Query

from deps import DBConn, CurrentUser, OptionalUser
from errors import AppError
from helpers import get_vault_checked
from schemas.note import NoteCreate, NoteDetail, NoteUpdate

router = APIRouter(tags=["notes"])

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


async def _get_note_or_raise(db, note_id: int) -> dict:
    row = await db.fetchrow(
        "SELECT id, title, content, vault_id, created_at, updated_at FROM notes WHERE id=$1",
        note_id,
    )
    if not row:
        raise AppError("NOT_FOUND", "找不到指定的 Note", 404)
    return dict(row)


async def _get_note_tags(db, note_id: int) -> list[dict]:
    rows = await db.fetch(
        "SELECT t.id, t.name FROM tags t JOIN note_tags nt ON nt.tag_id = t.id WHERE nt.note_id=$1",
        note_id,
    )
    return [dict(r) for r in rows]


async def _get_note_backlinks(db, note_id: int) -> list[dict]:
    rows = await db.fetch(
        "SELECT n.id, n.title FROM notes n JOIN links l ON l.src_note = n.id WHERE l.dest_note=$1",
        note_id,
    )
    return [dict(r) for r in rows]


async def _sync_note_tags(db, note_id: int, tag_names: list[str]) -> None:
    await db.execute("DELETE FROM note_tags WHERE note_id=$1", note_id)
    for name in tag_names:
        await db.execute("INSERT INTO tags(name) VALUES($1) ON CONFLICT(name) DO NOTHING", name)
    if tag_names:
        tag_rows = await db.fetch(
            "SELECT id FROM tags WHERE name = ANY($1::varchar[])", tag_names
        )
        for tag_row in tag_rows:
            await db.execute(
                "INSERT INTO note_tags(note_id, tag_id) VALUES($1,$2) ON CONFLICT DO NOTHING",
                note_id, tag_row["id"],
            )


async def _sync_links(db, note_id: int, vault_id: int, content: str) -> None:
    await db.execute("DELETE FROM links WHERE src_note=$1", note_id)
    titles = list(set(_WIKILINK_RE.findall(content)))
    for title in titles:
        dest = await db.fetchrow(
            "SELECT id FROM notes WHERE title=$1 AND vault_id=$2", title, vault_id
        )
        if dest:
            await db.execute(
                "INSERT INTO links(src_note, dest_note) VALUES($1,$2) ON CONFLICT DO NOTHING",
                note_id, dest["id"],
            )


async def _batch_tags(db, note_ids: list[int]) -> dict[int, list]:
    tags_by_note: dict[int, list] = {nid: [] for nid in note_ids}
    if note_ids:
        rows = await db.fetch(
            "SELECT nt.note_id, t.id, t.name FROM note_tags nt JOIN tags t ON t.id = nt.tag_id"
            " WHERE nt.note_id = ANY($1::int[])",
            note_ids,
        )
        for r in rows:
            tags_by_note[r["note_id"]].append({"id": r["id"], "name": r["name"]})
    return tags_by_note


@router.get("/vaults/{vault_id}/notes")
async def list_notes(
    vault_id: int,
    db: DBConn,
    user: OptionalUser,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    await get_vault_checked(db, vault_id, user)
    offset = (page - 1) * size
    rows = await db.fetch(
        "SELECT id, title, vault_id, created_at, updated_at, COUNT(*) OVER() AS total"
        " FROM notes WHERE vault_id=$1 ORDER BY updated_at DESC LIMIT $2 OFFSET $3",
        vault_id, size, offset,
    )
    total = int(rows[0]["total"]) if rows else 0
    note_ids = [r["id"] for r in rows]
    tags_by_note = await _batch_tags(db, note_ids)
    items = [
        {"id": r["id"], "title": r["title"], "vault_id": r["vault_id"],
         "created_at": r["created_at"], "updated_at": r["updated_at"],
         "tags": tags_by_note[r["id"]]}
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "size": size, "pages": math.ceil(total / size) if total else 0}


@router.get("/notes/{note_id}", response_model=NoteDetail)
async def get_note(note_id: int, db: DBConn, user: OptionalUser):
    note = await _get_note_or_raise(db, note_id)
    vault_row = await db.fetchrow("SELECT public, owner FROM vaults WHERE id=$1", note["vault_id"])
    if not vault_row["public"]:
        if not user or user["id"] != vault_row["owner"]:
            raise AppError("FORBIDDEN", "無權限存取此 Note", 403)
    tags = await _get_note_tags(db, note_id)
    backlinks = await _get_note_backlinks(db, note_id)
    return {**note, "tags": tags, "backlinks": backlinks}


@router.post("/notes", status_code=201, response_model=NoteDetail)
async def create_note(body: NoteCreate, db: DBConn, current_user: CurrentUser):
    await get_vault_checked(db, body.vault_id, current_user, require_owner=True)
    row = await db.fetchrow(
        "INSERT INTO notes(vault_id, title, content) VALUES($1,$2,$3)"
        " RETURNING id, title, content, vault_id, created_at, updated_at",
        body.vault_id, body.title, body.content,
    )
    note = dict(row)
    await _sync_note_tags(db, note["id"], body.tags)
    await _sync_links(db, note["id"], body.vault_id, body.content)
    tags = await _get_note_tags(db, note["id"])
    return {**note, "tags": tags, "backlinks": []}


@router.patch("/notes/{note_id}", response_model=NoteDetail)
async def update_note(note_id: int, body: NoteUpdate, db: DBConn, current_user: CurrentUser):
    note = await _get_note_or_raise(db, note_id)
    vault_row = await db.fetchrow("SELECT owner FROM vaults WHERE id=$1", note["vault_id"])
    if vault_row["owner"] != current_user["id"]:
        raise AppError("FORBIDDEN", "無權限修改此 Note", 403)

    updates: list[str] = []
    params: list = []
    if body.title is not None:
        params.append(body.title)
        updates.append(f"title=${len(params)}")
    if body.content is not None:
        params.append(body.content)
        updates.append(f"content=${len(params)}")

    if updates:
        params.append(note_id)
        row = await db.fetchrow(
            f"UPDATE notes SET {', '.join(updates)} WHERE id=${len(params)}"
            " RETURNING id, title, content, vault_id, created_at, updated_at",
            *params,
        )
        note = dict(row)

    if body.tags is not None:
        await _sync_note_tags(db, note_id, body.tags)
    if body.content is not None:
        await _sync_links(db, note_id, note["vault_id"], body.content)

    tags = await _get_note_tags(db, note_id)
    backlinks = await _get_note_backlinks(db, note_id)
    return {**note, "tags": tags, "backlinks": backlinks}


@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, db: DBConn, current_user: CurrentUser):
    note = await _get_note_or_raise(db, note_id)
    vault_row = await db.fetchrow("SELECT owner FROM vaults WHERE id=$1", note["vault_id"])
    if vault_row["owner"] != current_user["id"]:
        raise AppError("FORBIDDEN", "無權限刪除此 Note", 403)
    await db.execute("DELETE FROM notes WHERE id=$1", note_id)
