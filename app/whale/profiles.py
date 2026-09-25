from dataclasses import dataclass

from app.db.models.wallet import Wallet


def short_address(address: str) -> str:
    if not address or len(address) < 8:
        return address
    return f"{address[:4]}...{address[-3:]}"


@dataclass
class WhaleProfile:
    address: str
    short: str
    pnl: float
    roi: float
    win_rate: float
    volume: float
    trade_count: int
    score: float | None
    sports: dict[str, float]


def from_wallet(wallet: Wallet, sports: dict[str, float] | None = None) -> WhaleProfile:
    return WhaleProfile(
        address=wallet.address,
        short=short_address(wallet.address),
        pnl=float(wallet.pnl or 0),
        roi=float(wallet.roi or 0),
        win_rate=float(wallet.win_rate or 0),
        volume=float(wallet.volume or 0),
        trade_count=int(wallet.trade_count or 0),
        score=float(wallet.whale_score) if wallet.whale_score is not None else None,
        sports=sports or {},
    )
