from datetime import datetime

from pydantic import BaseModel, Field


class VaultCreate(BaseModel):
    name: str = Field(..., max_length=255, examples=["My Linux Notes"])
    public: bool = Field(default=False, examples=[True])


class VaultUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255, examples=["Updated Vault Name"])
    public: bool | None = Field(default=None, examples=[False])


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
