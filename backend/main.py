from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

import database
from errors import AppError, app_error_handler, validation_error_handler
from routers import auth, notes, search, tags, vaults


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.create_pool()
    yield
    await database.close_pool()


app = FastAPI(title="leaflink-online API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
