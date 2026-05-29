import math
from typing import Annotated

from fastapi import APIRouter, Query

from deps import DBConn, CurrentUser, OptionalUser
from helpers import get_vault_checked
from schemas.vault import VaultCreate, VaultDetailResponse, VaultUpdate

router = APIRouter(tags=["vaults"])


@router.get("/vaults/mine")
async def get_my_vaults(
    db: DBConn,
    current_user: CurrentUser,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    offset = (page - 1) * size
    rows = await db.fetch(
        "SELECT id, name, public, created_at, COUNT(*) OVER() AS total"
        " FROM vaults WHERE owner=$1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
        current_user["id"], size, offset,
    )
    total = int(rows[0]["total"]) if rows else 0
    items = [{"id": r["id"], "name": r["name"], "public": r["public"], "created_at": r["created_at"]} for r in rows]
    return {"items": items, "total": total, "page": page, "size": size, "pages": math.ceil(total / size) if total else 0}


@router.get("/vaults/explore")
async def explore_vaults(
    db: DBConn,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    offset = (page - 1) * size
    rows = await db.fetch(
        "SELECT v.id, v.name, v.public, v.created_at, u.username AS owner_username, COUNT(*) OVER() AS total"
        " FROM vaults v JOIN users u ON u.id = v.owner WHERE v.public = TRUE"
        " ORDER BY v.created_at DESC LIMIT $1 OFFSET $2",
        size, offset,
    )
    total = int(rows[0]["total"]) if rows else 0
    items = [
        {"id": r["id"], "name": r["name"], "public": r["public"],
         "owner_username": r["owner_username"], "created_at": r["created_at"]}
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "size": size, "pages": math.ceil(total / size) if total else 0}


@router.get("/vaults/{vault_id}", response_model=VaultDetailResponse)
async def get_vault(vault_id: int, db: DBConn, user: OptionalUser):
    return await get_vault_checked(db, vault_id, user)


@router.post("/vaults", status_code=201, response_model=VaultDetailResponse)
async def create_vault(body: VaultCreate, db: DBConn, current_user: CurrentUser):
    row = await db.fetchrow(
        "INSERT INTO vaults(owner, name, public) VALUES($1,$2,$3)"
        " RETURNING id, name, public, owner, created_at",
        current_user["id"], body.name, body.public,
    )
    return {**dict(row), "owner_username": current_user["username"]}


@router.patch("/vaults/{vault_id}", response_model=VaultDetailResponse)
async def update_vault(vault_id: int, body: VaultUpdate, db: DBConn, current_user: CurrentUser):
    vault = await get_vault_checked(db, vault_id, current_user, require_owner=True)

    updates: list[str] = []
    params: list = []
    if body.name is not None:
        params.append(body.name)
        updates.append(f"name=${len(params)}")
    if body.public is not None:
        params.append(body.public)
        updates.append(f"public=${len(params)}")

    if not updates:
        return vault

    params.append(vault_id)
    row = await db.fetchrow(
        f"UPDATE vaults SET {', '.join(updates)} WHERE id=${len(params)}"
        " RETURNING id, name, public, owner, created_at",
        *params,
    )
    return {**dict(row), "owner_username": current_user["username"]}


@router.delete("/vaults/{vault_id}", status_code=204)
async def delete_vault(vault_id: int, db: DBConn, current_user: CurrentUser):
    await get_vault_checked(db, vault_id, current_user, require_owner=True)
    await db.execute("DELETE FROM vaults WHERE id=$1", vault_id)
