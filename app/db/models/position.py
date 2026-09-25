from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("wallet_id", "market_id", "outcome"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), nullable=False)
    outcome: Mapped[str] = mapped_column(Text, nullable=False)
    size: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    average_entry: Mapped[float | None] = mapped_column(Numeric(12, 6))
    current_price: Mapped[float | None] = mapped_column(Numeric(12, 6))
    unrealized_pnl: Mapped[float | None] = mapped_column(Numeric(24, 6))
    realized_pnl: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
