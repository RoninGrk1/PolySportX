from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Market(Base):
    __tablename__ = "markets"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    condition_id: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    event_id: Mapped[str | None] = mapped_column(Text)
    slug: Mapped[str | None] = mapped_column(Text)
    sport: Mapped[str | None] = mapped_column(Text)
    league: Mapped[str | None] = mapped_column(Text)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str | None] = mapped_column(Text)
    token_yes: Mapped[str | None] = mapped_column(Text)
    token_no: Mapped[str | None] = mapped_column(Text)
    price_yes: Mapped[float | None] = mapped_column(Numeric(12, 6))
    price_no: Mapped[float | None] = mapped_column(Numeric(12, 6))
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    volume: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    volume_24h: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    liquidity: Mapped[float] = mapped_column(Numeric(24, 6), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
