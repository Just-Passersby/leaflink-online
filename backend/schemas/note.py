from datetime import datetime

from pydantic import BaseModel


class TagRef(BaseModel):
    id: int
    name: str


class BacklinkRef(BaseModel):
    id: int
    title: str


class NoteCreate(BaseModel):
    vault_id: int
    title: str
    content: str = ""
    tags: list[str] = []


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


class NoteDetail(BaseModel):
    id: int
    title: str
    content: str
    vault_id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagRef]
    backlinks: list[BacklinkRef]
