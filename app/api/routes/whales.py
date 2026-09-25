from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session
from app.services.whale_service import WhaleService

router = APIRouter()


def _wallet(w) -> dict:
    return {
        "id": w.id,
        "address": w.address,
        "alias": w.alias,
        "whale_score": float(w.whale_score) if w.whale_score is not None else None,
        "pnl": float(w.pnl or 0),
        "roi": float(w.roi or 0),
        "volume": float(w.volume or 0),
        "win_rate": float(w.win_rate or 0),
        "trade_count": w.trade_count,
    }


@router.get("/whales")
async def list_whales(session: AsyncSession = Depends(db_session)):
    return [_wallet(w) for w in await WhaleService(session).list_whales()]


@router.get("/whales/top")
async def top_whales(session: AsyncSession = Depends(db_session)):
    rows = await WhaleService(session).top()
    return [
        {
            "rank": r.rank,
            "wallet_id": r.wallet_id,
            "score": float(r.score),
            "pnl": float(r.pnl or 0),
            "roi": float(r.roi or 0),
            "volume": float(r.volume or 0),
            "calculated_at": r.calculated_at,
        }
        for r in rows
    ]


@router.get("/whales/{address}")
async def get_whale(address: str, session: AsyncSession = Depends(db_session)):
    wallet = await WhaleService(session).by_address(address)
    if wallet is None:
        return {"error": "not_found"}
    return _wallet(wallet)


@router.get("/whales/{address}/trades")
async def whale_trades(address: str, session: AsyncSession = Depends(db_session)):
    svc = WhaleService(session)
    wallet = await svc.by_address(address)
    if wallet is None:
        return []
    trades = await svc.trades(wallet.id)
    return [
        {
            "id": t.id,
            "side": t.side,
            "outcome": t.outcome,
            "price": float(t.price),
            "size": float(t.size),
            "notional": float(t.notional),
            "timestamp": t.timestamp,
        }
        for t in trades
    ]


@router.get("/whales/{address}/positions")
async def whale_positions(address: str, session: AsyncSession = Depends(db_session)):
    svc = WhaleService(session)
    wallet = await svc.by_address(address)
    if wallet is None:
        return []
    positions = await svc.positions(wallet.id)
    return [
        {
            "market_id": p.market_id,
            "outcome": p.outcome,
            "size": float(p.size),
            "average_entry": float(p.average_entry) if p.average_entry is not None else None,
            "unrealized_pnl": float(p.unrealized_pnl or 0),
            "realized_pnl": float(p.realized_pnl or 0),
        }
        for p in positions
    ]
