from app.polymarket.clob import ClobClient
from app.polymarket.data_api import DataApiClient
from app.polymarket.gamma import GammaClient


class PolymarketClient:
    """Facade so API changes stay behind one internal interface."""

    def __init__(self) -> None:
        self.gamma = GammaClient()
        self.clob = ClobClient()
        self.data = DataApiClient()

    async def ping(self) -> bool:
        try:
            await self.gamma.get_sports()
            return True
        except Exception:
            try:
                await self.gamma.get_markets(limit=1)
                return True
            except Exception:
                return False
