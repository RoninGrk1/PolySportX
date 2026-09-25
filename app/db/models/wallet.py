from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    alias: Mapped[str | None] = mapped_column(Text)
    whale_score: Mapped[float | None] = mapped_column(Numeric(10, 4))
    pnl: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    roi: Mapped[float] = mapped_column(Numeric(12, 6), default=0)
    volume: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    win_rate: Mapped[float] = mapped_column(Numeric(8, 6), default=0)
    trade_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_trade_size: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    sports_exposure: Mapped[float] = mapped_column(Numeric(8, 6), default=0)
    active_days: Mapped[int] = mapped_column(Integer, default=0)
    first_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class WhaleScore(Base):
    __tablename__ = "whale_scores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    period: Mapped[str] = mapped_column(String(16), nullable=False)
    pnl: Mapped[float | None] = mapped_column(Numeric(24, 6))
    roi: Mapped[float | None] = mapped_column(Numeric(12, 6))
    volume: Mapped[float | None] = mapped_column(Numeric(24, 6))
    win_rate: Mapped[float | None] = mapped_column(Numeric(8, 6))
    consistency: Mapped[float | None] = mapped_column(Numeric(8, 4))
    timing_score: Mapped[float | None] = mapped_column(Numeric(8, 4))
    roi_score: Mapped[float | None] = mapped_column(Numeric(8, 4))
    pnl_score: Mapped[float | None] = mapped_column(Numeric(8, 4))
    recent_score: Mapped[float | None] = mapped_column(Numeric(8, 4))
    activity_score: Mapped[float | None] = mapped_column(Numeric(8, 4))
    score: Mapped[float | None] = mapped_column(Numeric(8, 4))
    rank: Mapped[int | None] = mapped_column(Integer)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RankingSnapshot(Base):
    __tablename__ = "ranking_snapshots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    period: Mapped[str] = mapped_column(String(16), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    pnl: Mapped[float | None] = mapped_column(Numeric(24, 6))
    roi: Mapped[float | None] = mapped_column(Numeric(12, 6))
    volume: Mapped[float | None] = mapped_column(Numeric(24, 6))
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
