import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import database
from errors import AppError, app_error_handler, validation_error_handler
from routers import auth, notes, search, tags, vaults

_TAGS_METADATA = [
    {"name": "auth", "description": "使用者認證：註冊、登入、登出、查詢目前登入狀態。"},
    {"name": "vaults", "description": "Vault CRUD 與公開 Vault 瀏覽。"},
    {
        "name": "notes",
        "description": "筆記 CRUD，含 `[[雙向連結]]` 自動解析與 backlinks 查詢。",
    },
    {"name": "tags", "description": "標籤查詢，供前端搜尋 autocomplete 使用。"},
    {"name": "search", "description": "PostgreSQL `tsvector` 全文搜尋。"},
]

_DESCRIPTION = """
Obsidian 風格的線上筆記系統 API。

## 認證方式

JWT 存放於 `access_token` **HttpOnly Cookie**（7 天有效期）。
所有需要認證的端點請先呼叫 `POST /auth/login` 取得 cookie。

## 錯誤格式

所有錯誤統一回傳：
```json
{ "code": "ERROR_CODE", "message": "說明", "detail": null }
```
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.create_pool()
    yield
    await database.close_pool()


app = FastAPI(
    title="leaflink-online API",
    version="0.1.0",
    description=_DESCRIPTION,
    openapi_tags=_TAGS_METADATA,
    lifespan=lifespan,
)

_default_origins = "http://localhost:5173,http://localhost"
_origins = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", _default_origins).split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(auth.router)
app.include_router(vaults.router)
app.include_router(notes.router)
app.include_router(tags.router)
app.include_router(search.router)
