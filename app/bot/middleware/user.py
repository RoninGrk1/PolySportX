from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.db.database import SessionLocal
from app.services.user_service import UserService


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is not None:
            async with SessionLocal() as session:
                svc = UserService(session)
                data["db_user"] = await svc.onboard(user.id, user.username)
        return await handler(event, data)
