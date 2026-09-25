from __future__ import annotations

from dataclasses import dataclass


NEW_POSITION = "NEW_POSITION"
POSITION_INCREASE = "POSITION_INCREASE"
POSITION_DECREASE = "POSITION_DECREASE"
PARTIAL_EXIT = "PARTIAL_EXIT"
FULL_EXIT = "FULL_EXIT"
REVERSAL = "REVERSAL"


@dataclass
class PositionState:
    size: float
    average_entry: float | None
    current_price: float | None
    unrealized_pnl: float
    realized_pnl: float


def apply_trade(
    previous_size: float,
    previous_avg: float | None,
    previous_realized: float,
    side: str,
    price: float,
    size: float,
    current_price: float | None = None,
) -> PositionState:
    side = side.upper()
    price = float(price)
    size = float(size)
    prev = float(previous_size or 0)
    avg = float(previous_avg) if previous_avg is not None else None
    realized = float(previous_realized or 0)

    if side == "BUY":
        new_size = prev + size
        if new_size <= 0:
            new_size = 0.0
            avg = None
        elif prev <= 0 or avg is None:
            avg = price
        else:
            avg = ((prev * avg) + (size * price)) / new_size
    else:
        sell = min(size, prev) if prev > 0 else 0.0
        if avg is not None and sell > 0:
            realized += (price - avg) * sell
        new_size = max(prev - size, 0.0)
        if new_size == 0:
            avg = None

    mark = current_price if current_price is not None else price
    unrealized = 0.0
    if new_size > 0 and avg is not None and mark is not None:
        unrealized = (float(mark) - avg) * new_size

    return PositionState(
        size=round(new_size, 8),
        average_entry=None if avg is None else round(avg, 8),
        current_price=None if mark is None else float(mark),
        unrealized_pnl=round(unrealized, 6),
        realized_pnl=round(realized, 6),
    )


def detect_event(previous_size: float, current_size: float, side: str | None = None) -> str:
    prev = float(previous_size or 0)
    curr = float(current_size or 0)
    if prev == 0 and curr > 0:
        return NEW_POSITION
    if curr == 0 and prev > 0:
        return FULL_EXIT
    if curr > prev:
        return POSITION_INCREASE
    if 0 < curr < prev:
        if side and side.upper() == "SELL":
            return PARTIAL_EXIT
        return POSITION_DECREASE
    return POSITION_DECREASE if curr != prev else "NO_CHANGE"


def is_large_trade(notional: float, avg_trade_size: float | None, global_min: float, multiplier: float) -> bool:
    if notional >= global_min:
        return True
    if avg_trade_size and avg_trade_size > 0 and notional >= avg_trade_size * multiplier:
        return True
    return False
