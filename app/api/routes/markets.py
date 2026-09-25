from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session
from app.services.market_service import MarketService

router = APIRouter()


def _dump(market) -> dict:
    return {
        "id": market.id,
        "condition_id": market.condition_id,
        "event_id": market.event_id,
        "slug": market.slug,
        "sport": market.sport,
        "league": market.league,
        "question": market.question,
        "status": market.status,
        "token_yes": market.token_yes,
        "token_no": market.token_no,
        "price_yes": float(market.price_yes) if market.price_yes is not None else None,
        "price_no": float(market.price_no) if market.price_no is not None else None,
        "volume": float(market.volume or 0),
        "volume_24h": float(market.volume_24h or 0),
        "liquidity": float(market.liquidity or 0),
        "start_time": market.start_time,
        "end_time": market.end_time,
    }


@router.get("/markets")
async def list_markets(sport: str | None = None, session: AsyncSession = Depends(db_session)):
    rows = await MarketService(session).list_markets(sport=sport)
    return [_dump(m) for m in rows]


@router.get("/markets/{market_id}")
async def get_market(market_id: int, session: AsyncSession = Depends(db_session)):
    market = await MarketService(session).get(market_id)
    if market is None:
        return {"error": "not_found"}
    return _dump(market)
