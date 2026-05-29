from datetime import datetime

from pydantic import BaseModel, Field


class TagRef(BaseModel):
    id: int
    name: str


class BacklinkRef(BaseModel):
    id: int
    title: str


class NoteCreate(BaseModel):
    vault_id: int = Field(..., examples=[1])
    title: str = Field(..., max_length=255, examples=["Hello World"])
    content: str = Field(default="", examples=["# Hello\n\n連結到 [[Other Note]]"])
    tags: list[str] = Field(default=[], examples=[["linux", "btrfs"]])


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255, examples=["Updated Title"])
    content: str | None = Field(default=None, examples=["# Updated\n\n新內容"])
    tags: list[str] | None = Field(default=None, examples=[["linux"]])


class NoteListItem(BaseModel):
    id: int
    title: str
    vault_id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagRef]


class NoteDetail(BaseModel):
    id: int
    title: str
    content: str
    vault_id: int
    created_at: datetime
    updated_at: datetime
    tags: list[TagRef]
    backlinks: list[BacklinkRef]


class SearchResultItem(BaseModel):
    id: int
    title: str
    vault_id: int
    vault_name: str
    owner_username: str
    updated_at: datetime
    tags: list[TagRef]
