from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session
from app.db.repositories.alerts import AlertRepository
from app.db.repositories.users import UserRepository

router = APIRouter()


@router.get("/users/{telegram_id}/alerts")
async def user_alerts(telegram_id: int, session: AsyncSession = Depends(db_session)):
    user = await UserRepository(session).get_by_telegram_id(telegram_id)
    if user is None:
        return []
    rows = await AlertRepository(session).for_user(user.id)
    return [
        {
            "id": a.id,
            "alert_type": a.alert_type,
            "signal_strength": a.signal_strength,
            "payload": a.payload,
            "sent_at": a.sent_at,
        }
        for a in rows
    ]
