from fastapi import APIRouter

from deps import DBConn

router = APIRouter(tags=["tags"])


@router.get("/tags")
async def list_tags(db: DBConn):
    rows = await db.fetch("SELECT id, name FROM tags ORDER BY name")
    return [dict(r) for r in rows]
