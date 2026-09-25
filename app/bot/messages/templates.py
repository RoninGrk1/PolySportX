from app.alerts.templates import money, pct
from app.config.sports import sport_emoji
from app.whale.profiles import short_address


START = (
    "PolySportX\n"
    "Polymarket Sports Intelligence\n"
    "Track markets.\n"
    "Track whales.\n"
    "Receive smart-money alerts."
)


def market_card(market) -> str:
    emoji = sport_emoji(getattr(market, "sport", None))
    yes = getattr(market, "price_yes", None)
    no = getattr(market, "price_no", None)
    yes_txt = f"{int(float(yes)*100)}c" if yes is not None else "-"
    no_txt = f"{int(float(no)*100)}c" if no is not None else "-"
    return (
        f"{emoji} {market.question}\n"
        f"YES {yes_txt}   NO {no_txt}\n"
        f"24h volume {money(float(getattr(market, 'volume_24h', 0) or market.volume or 0))}\n"
        f"Liquidity {money(float(market.liquidity or 0))}"
    )


def top5_card(rows: list[tuple[int, object]]) -> str:
    lines = ["TOP 5 SPORTS WHALES"]
    for rank, wallet in rows:
        lines.append(
            f"{rank}. {short_address(wallet.address)}\n"
            f"   P&L: {money(float(wallet.pnl or 0))}\n"
            f"   ROI: {pct(float(wallet.roi or 0))}\n"
            f"   Volume: {money(float(wallet.volume or 0))}"
        )
    if len(lines) == 1:
        lines.append("No ranked whales yet. Workers are still ingesting data.")
    return "\n".join(lines)


def whale_card(wallet, sports: dict[str, float] | None = None) -> str:
    lines = [
        "WHALE PROFILE",
        f"Wallet\n{short_address(wallet.address)}",
        f"30D P&L     {money(float(wallet.pnl or 0))}",
        f"30D ROI     {pct(float(wallet.roi or 0))}",
        f"Win Rate    {float(wallet.win_rate or 0)*100:.0f}%",
        f"Volume      {money(float(wallet.volume or 0))}",
        f"Trades      {int(wallet.trade_count or 0)}",
        "Sports:",
    ]
    if sports:
        for name, share in sports.items():
            lines.append(f"{name.upper()}  {share*100:.0f}%")
    else:
        lines.append("NBA / NFL mix -- updating")
    return "\n".join(lines)
