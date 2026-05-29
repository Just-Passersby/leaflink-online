from fastapi import APIRouter

from deps import DBConn
from schemas.tag import TagResponse

router = APIRouter(tags=["tags"])


@router.get("/tags", response_model=list[TagResponse], summary="取得所有標籤")
async def list_tags(db: DBConn):
    """回傳所有 tag，供前端搜尋 autocomplete 使用。不分頁。"""
    rows = await db.fetch("SELECT id, name FROM tags ORDER BY name")
    return [dict(r) for r in rows]
