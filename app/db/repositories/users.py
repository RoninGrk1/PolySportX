from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserWallet


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        res = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return res.scalar_one_or_none()

    async def upsert(self, telegram_id: int, username: str | None = None) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            if username is not None:
                user.username = username
            return user
        user = User(telegram_id=telegram_id, username=username)
        self.session.add(user)
        await self.session.flush()
        return user

    async def follow(self, user_id: int, wallet_id: int) -> UserWallet:
        res = await self.session.execute(
            select(UserWallet).where(
                UserWallet.user_id == user_id, UserWallet.wallet_id == wallet_id
            )
        )
        existing = res.scalar_one_or_none()
        if existing:
            existing.enabled = True
            return existing
        row = UserWallet(user_id=user_id, wallet_id=wallet_id)
        self.session.add(row)
        await self.session.flush()
        return row

    async def unfollow(self, user_id: int, wallet_id: int) -> bool:
        res = await self.session.execute(
            select(UserWallet).where(
                UserWallet.user_id == user_id, UserWallet.wallet_id == wallet_id
            )
        )
        row = res.scalar_one_or_none()
        if not row:
            return False
        row.enabled = False
        return True

    async def watchlist(self, user_id: int) -> list[UserWallet]:
        res = await self.session.execute(
            select(UserWallet).where(UserWallet.user_id == user_id, UserWallet.enabled.is_(True))
        )
        return list(res.scalars())

    async def followers_of(self, wallet_id: int) -> list[UserWallet]:
        res = await self.session.execute(
            select(UserWallet).where(UserWallet.wallet_id == wallet_id, UserWallet.enabled.is_(True))
        )
        return list(res.scalars())

    async def all_alert_users(self) -> list[User]:
        res = await self.session.execute(select(User))
        return list(res.scalars())
