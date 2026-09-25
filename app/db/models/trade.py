from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    external_id: Mapped[str | None] = mapped_column(Text, unique=True)
    wallet_id: Mapped[int | None] = mapped_column(ForeignKey("wallets.id"))
    market_id: Mapped[int | None] = mapped_column(ForeignKey("markets.id"))
    side: Mapped[str] = mapped_column(Text, nullable=False)
    outcome: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 6), nullable=False)
    size: Mapped[float] = mapped_column(Numeric(24, 6), nullable=False)
    notional: Mapped[float] = mapped_column(Numeric(24, 6), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    tx_hash: Mapped[str | None] = mapped_column(Text)
