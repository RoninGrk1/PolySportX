from app.config.sports import sport_emoji
from app.whale.profiles import short_address


def money(value: float) -> str:
    sign = "+" if value > 0 else ""
    if abs(value) >= 1_000_000:
        return f"{sign}${value/1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{sign}${value/1_000:.1f}K"
    return f"{sign}${value:,.0f}"


def pct(value: float) -> str:
    return f"{value*100:+.1f}%"


def whale_alert(
    *,
    sport: str | None,
    question: str,
    address: str,
    side: str,
    outcome: str,
    size: float,
    entry: float,
    current: float | None,
    position: float,
    roi: float,
    strength: str,
) -> str:
    emoji = sport_emoji(sport)
    current_txt = f"{int(current*100)}c" if current is not None else "-"
    return (
        "WHALE MOVE\n"
        f"{emoji} {question}\n"
        f"{short_address(address)}\n"
        f"{side.upper()} -- {outcome}\n"
        f"Size\n{money(size)}\n"
        f"Entry\n{int(entry*100)}c\n"
        f"Current\n{current_txt}\n"
        f"Position\n{money(position)}\n"
        f"30D ROI\n{pct(roi)}\n"
        f"Signal\n{strength}\n"
        "\nObserved activity -- not a guaranteed outcome."
    )


def consensus_alert(*, question: str, count: int, notional: float, outcome: str) -> str:
    return (
        "WHALE CONSENSUS\n"
        f"{question}\n"
        f"{count} tracked whales\n"
        f"{money(notional)} combined exposure\n"
        f"Outcome: {outcome}\n"
        "\nObserved activity -- not a guaranteed outcome."
    )
