from collections.abc import AsyncGenerator

from fastapi import Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.db.database import get_session


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


def require_admin(x_admin_key: str | None = Header(default=None)) -> None:
    if not x_admin_key or x_admin_key != settings.admin_api_key:
        raise HTTPException(status_code=401, detail="unauthorized")
