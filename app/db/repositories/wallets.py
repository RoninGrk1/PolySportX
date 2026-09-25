from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.wallet import Wallet


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_address(self, address: str) -> Wallet | None:
        res = await self.session.execute(
            select(Wallet).where(Wallet.address == address.lower())
        )
        return res.scalar_one_or_none()

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        return await self.session.get(Wallet, wallet_id)

    async def upsert(self, address: str, **fields) -> Wallet:
        address = address.lower()
        wallet = await self.get_by_address(address)
        if wallet is None:
            wallet = Wallet(address=address)
            self.session.add(wallet)
        for k, v in fields.items():
            if v is not None and hasattr(wallet, k):
                setattr(wallet, k, v)
        await self.session.flush()
        return wallet

    async def list_all(self, limit: int = 100) -> list[Wallet]:
        res = await self.session.execute(
            select(Wallet).order_by(Wallet.whale_score.desc().nullslast()).limit(limit)
        )
        return list(res.scalars())
