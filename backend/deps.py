from typing import Annotated

import jwt
from fastapi import Cookie, Depends

import database
from config import settings
from errors import AppError


async def get_db():
    async with database.pool.acquire() as conn:
        yield conn


def _decode_token(token: str | None) -> dict | None:
    if not token:
        return None
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None


async def get_current_user(access_token: str | None = Cookie(default=None)) -> dict:
    payload = _decode_token(access_token)
    if not payload:
        raise AppError("UNAUTHORIZED", "未登入或 token 失效", 401)
    return {"id": int(payload["sub"]), "username": payload["username"], "email": payload["email"]}


async def get_optional_user(access_token: str | None = Cookie(default=None)) -> dict | None:
    payload = _decode_token(access_token)
    if not payload:
        return None
    return {"id": int(payload["sub"]), "username": payload["username"], "email": payload["email"]}


DBConn = Annotated[object, Depends(get_db)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
OptionalUser = Annotated[dict | None, Depends(get_optional_user)]
