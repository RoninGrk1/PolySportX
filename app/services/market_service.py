from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.markets import MarketRepository


class MarketService:
    def __init__(self, session: AsyncSession):
        self.repo = MarketRepository(session)

    async def list_markets(self, sport: str | None = None, limit: int = 50):
        return await self.repo.list_sports(sport=sport, limit=limit)

    async def get(self, market_id: int):
        return await self.repo.get_by_id(market_id)
