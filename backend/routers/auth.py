from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Response

from config import settings
from deps import DBConn, CurrentUser
from errors import AppError
from schemas.auth import LoginRequest, RegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def _create_token(user_id: int, username: str, email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_expire_days)
    return jwt.encode(
        {"sub": str(user_id), "username": username, "email": email, "exp": expire},
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def _set_auth_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        "access_token",
        token,
        max_age=settings.jwt_expire_days * 86400,
        httponly=True,
        samesite="lax",
    )


@router.post("/register", response_model=UserResponse)
async def register(body: RegisterRequest, response: Response, db: DBConn):
    existing = await db.fetchrow(
        "SELECT id FROM users WHERE username=$1 OR email=$2",
        body.username,
        body.email,
    )
    if existing:
        raise AppError("CONFLICT", "username 或 email 已存在", 409)

    pw_hash = _hash_password(body.password)
    row = await db.fetchrow(
        "INSERT INTO users(username, email, password_hash) VALUES($1,$2,$3)"
        " RETURNING id, username, email, created_at",
        body.username,
        body.email,
        pw_hash,
    )
    _set_auth_cookie(response, _create_token(row["id"], row["username"], row["email"]))
    return dict(row)


@router.post("/login", response_model=UserResponse)
async def login(body: LoginRequest, response: Response, db: DBConn):
    row = await db.fetchrow(
        "SELECT id, username, email, password_hash, created_at FROM users WHERE username=$1",
        body.username,
    )
    if not row or not _verify_password(body.password, row["password_hash"]):
        raise AppError("UNAUTHORIZED", "帳號或密碼錯誤", 401)

    _set_auth_cookie(response, _create_token(row["id"], row["username"], row["email"]))
    return {"id": row["id"], "username": row["username"], "email": row["email"], "created_at": row["created_at"]}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "登出成功"}


@router.get("/me", response_model=UserResponse)
async def me(current_user: CurrentUser, db: DBConn):
    row = await db.fetchrow(
        "SELECT id, username, email, created_at FROM users WHERE id=$1",
        current_user["id"],
    )
    if not row:
        raise AppError("UNAUTHORIZED", "使用者不存在", 401)
    return dict(row)
