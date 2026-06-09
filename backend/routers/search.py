from typing import Annotated

from fastapi import APIRouter, Query

from deps import DBConn, OptionalUser
from schemas.common import PagedResponse
from schemas.note import SearchResultItem

router = APIRouter(tags=["search"])


@router.get("/search", response_model=PagedResponse[SearchResultItem], summary="全文搜尋筆記")
async def search_notes(
    db: DBConn,
    user: OptionalUser,
    q: Annotated[str, Query(min_length=1, description="搜尋關鍵字")],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    """
    使用 PostgreSQL `tsvector` 全文搜尋。

    - 未登入：只搜尋公開 Vault 的筆記
    - 已登入：搜尋公開 Vault + 自己的 Private Vault
    """
    offset = (page - 1) * size
    base = (
        "SELECT n.id, n.title, n.vault_id, v.name AS vault_name, u.username AS owner_username,"
        " n.updated_at, COUNT(*) OVER() AS total"
        " FROM notes n JOIN vaults v ON v.id = n.vault_id JOIN users u ON u.id = v.owner"
        " WHERE (n.search_vector @@ plainto_tsquery('simple', $1)"
        "   OR n.title ILIKE '%' || $1 || '%' OR n.content ILIKE '%' || $1 || '%')"
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
    return PagedResponse.build(items, total, page, size)
