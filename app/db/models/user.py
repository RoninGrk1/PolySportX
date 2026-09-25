from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(Text)
    subscription: Mapped[str] = mapped_column(String(32), default="free")
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    alert_large_trades: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_entries: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_exits: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_consensus: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_top5: Mapped[bool] = mapped_column(Boolean, default=True)
    min_trade_notional: Mapped[float] = mapped_column(Numeric(20, 4), default=5000)
    sports_filter: Mapped[list] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    watchlist: Mapped[list["UserWallet"]] = relationship(back_populates="user")


class UserWallet(Base):
    __tablename__ = "user_wallets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_large_trades: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_entries: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_exits: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_consensus: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="watchlist")
