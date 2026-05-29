import math
from typing import Annotated

from fastapi import APIRouter, Query

from deps import DBConn, OptionalUser

router = APIRouter(tags=["search"])


@router.get("/search")
async def search_notes(
    db: DBConn,
    user: OptionalUser,
    q: Annotated[str, Query(min_length=1)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    offset = (page - 1) * size
    base = (
        "SELECT n.id, n.title, n.vault_id, v.name AS vault_name, u.username AS owner_username,"
        " n.updated_at, COUNT(*) OVER() AS total"
        " FROM notes n JOIN vaults v ON v.id = n.vault_id JOIN users u ON u.id = v.owner"
        " WHERE n.search_vector @@ plainto_tsquery('simple', $1)"
    )

    if user:
        rows = await db.fetch(
            base + " AND (v.public = TRUE OR v.owner = $2) ORDER BY n.updated_at DESC LIMIT $3 OFFSET $4",
            q, user["id"], size, offset,
        )
    else:
        rows = await db.fetch(
            base + " AND v.public = TRUE ORDER BY n.updated_at DESC LIMIT $2 OFFSET $3",
            q, size, offset,
        )

    total = int(rows[0]["total"]) if rows else 0
    note_ids = [r["id"] for r in rows]

    tags_by_note: dict[int, list] = {r["id"]: [] for r in rows}
    if note_ids:
        tag_rows = await db.fetch(
            "SELECT nt.note_id, t.id, t.name FROM note_tags nt JOIN tags t ON t.id = nt.tag_id"
            " WHERE nt.note_id = ANY($1::int[])",
            note_ids,
        )
        for tr in tag_rows:
            tags_by_note[tr["note_id"]].append({"id": tr["id"], "name": tr["name"]})

    items = [
        {"id": r["id"], "title": r["title"], "vault_id": r["vault_id"],
         "vault_name": r["vault_name"], "owner_username": r["owner_username"],
         "updated_at": r["updated_at"], "tags": tags_by_note[r["id"]]}
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "size": size, "pages": math.ceil(total / size) if total else 0}
