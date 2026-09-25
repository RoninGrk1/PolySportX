from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.users import UserRepository
from app.db.repositories.wallets import WalletRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.users = UserRepository(session)
        self.wallets = WalletRepository(session)

    async def onboard(self, telegram_id: int, username: str | None = None):
        user = await self.users.upsert(telegram_id, username)
        await self.users.session.commit()
        return user

    async def follow_address(self, telegram_id: int, address: str):
        user = await self.users.upsert(telegram_id)
        wallet = await self.wallets.upsert(address)
        row = await self.users.follow(user.id, wallet.id)
        await self.users.session.commit()
        return row

    async def unfollow_address(self, telegram_id: int, address: str) -> bool:
        user = await self.users.get_by_telegram_id(telegram_id)
        wallet = await self.wallets.get_by_address(address.lower())
        if not user or not wallet:
            return False
        ok = await self.users.unfollow(user.id, wallet.id)
        await self.users.session.commit()
        return ok
