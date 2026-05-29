from errors import AppError


async def get_vault_checked(
    db, vault_id: int, user: dict | None, require_owner: bool = False
) -> dict:
    row = await db.fetchrow(
        "SELECT v.id, v.name, v.public, v.owner, v.created_at, u.username AS owner_username"
        " FROM vaults v JOIN users u ON u.id = v.owner WHERE v.id=$1",
        vault_id,
    )
    if not row:
        raise AppError("NOT_FOUND", "找不到指定的 Vault", 404)
    vault = dict(row)
    if require_owner:
        if not user or user["id"] != vault["owner"]:
            raise AppError("FORBIDDEN", "無權限操作此 Vault", 403)
    elif not vault["public"]:
        if not user or user["id"] != vault["owner"]:
            raise AppError("FORBIDDEN", "無權限存取此 Vault", 403)
    return vault
