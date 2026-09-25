from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session
from app.db.repositories.alerts import AlertRepository

router = APIRouter()


@router.get("/signals")
async def list_signals(session: AsyncSession = Depends(db_session)):
    rows = await AlertRepository(session).recent_signals()
    return [
        {
            "id": s.id,
            "event_type": s.event_type,
            "strength": s.strength,
            "score": s.score,
            "wallet_id": s.wallet_id,
            "market_id": s.market_id,
            "payload": s.payload,
            "created_at": s.created_at,
        }
        for s in rows
    ]


@router.get("/signals/{signal_id}")
async def get_signal(signal_id: int, session: AsyncSession = Depends(db_session)):
    row = await AlertRepository(session).get_signal(signal_id)
    if row is None:
        return {"error": "not_found"}
    return {
        "id": row.id,
        "event_type": row.event_type,
        "strength": row.strength,
        "score": row.score,
        "payload": row.payload,
    }
