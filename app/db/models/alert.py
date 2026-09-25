from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id"))
    market_id: Mapped[int | None] = mapped_column(ForeignKey("markets.id"))
    alert_type: Mapped[str] = mapped_column(Text, nullable=False)
    signal_strength: Mapped[str | None] = mapped_column(String(16))
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SignalEvent(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id"))
    market_id: Mapped[int | None] = mapped_column(ForeignKey("markets.id"))
    trade_id: Mapped[int | None] = mapped_column(ForeignKey("trades.id"))
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    strength: Mapped[str] = mapped_column(String(16), nullable=False)
    score: Mapped[int] = mapped_column()
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
