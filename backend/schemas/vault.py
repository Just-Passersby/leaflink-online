from datetime import datetime

from pydantic import BaseModel


class VaultCreate(BaseModel):
    name: str
    public: bool = False


class VaultUpdate(BaseModel):
    name: str | None = None
    public: bool | None = None


class VaultResponse(BaseModel):
    id: int
    name: str
    public: bool
    created_at: datetime


class VaultDetailResponse(BaseModel):
    id: int
    name: str
    public: bool
    owner_username: str
    created_at: datetime
