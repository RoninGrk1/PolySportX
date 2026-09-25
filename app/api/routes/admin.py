from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import db_session, require_admin
from app.collectors.markets import MarketCollector
from app.collectors.wallets import WalletCollector

router = APIRouter(prefix="/admin", dependencies=[Depends(require_admin)])


@router.post("/resync-markets")
async def resync_markets(session: AsyncSession = Depends(db_session)):
    count = await MarketCollector(session).sync_sports_markets()
    return {"synced": count}


@router.post("/rescan-wallet")
async def rescan_wallet(wallet_id: int, session: AsyncSession = Depends(db_session)):
    count = await WalletCollector(session).refresh_statistics(wallet_id=wallet_id)
    return {"updated": count}


@router.post("/recalculate-whales")
async def recalculate_whales(session: AsyncSession = Depends(db_session)):
    count = await WalletCollector(session).refresh_statistics()
    return {"updated": count}
