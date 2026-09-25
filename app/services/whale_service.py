from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.positions import PositionRepository
from app.db.repositories.trades import TradeRepository
from app.db.repositories.wallets import WalletRepository
from app.db.repositories.whales import WhaleRepository


class WhaleService:
    def __init__(self, session: AsyncSession):
        self.wallets = WalletRepository(session)
        self.whales = WhaleRepository(session)
        self.trades = TradeRepository(session)
        self.positions = PositionRepository(session)

    async def list_whales(self, limit: int = 50):
        return await self.wallets.list_all(limit=limit)

    async def top(self, period: str = "active", limit: int = 5):
        return await self.whales.latest_top(period=period, limit=limit)

    async def by_address(self, address: str):
        return await self.wallets.get_by_address(address.lower())

    async def trades(self, wallet_id: int, limit: int = 50):
        return await self.trades.for_wallet(wallet_id, limit=limit)

    async def positions(self, wallet_id: int):
        return await self.positions.for_wallet(wallet_id)
