import asyncpg

from config import settings

pool: asyncpg.Pool | None = None


async def create_pool() -> None:
    global pool
    pool = await asyncpg.create_pool(dsn=settings.database_url, min_size=2, max_size=10)


async def close_pool() -> None:
    global pool
    if pool:
        await pool.close()
        pool = None
