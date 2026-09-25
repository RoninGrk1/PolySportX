from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Live Markets", callback_data="markets:all")],
            [InlineKeyboardButton(text="Top 5 Whales", callback_data="whales:top")],
            [InlineKeyboardButton(text="Whale Alerts", callback_data="alerts:home")],
            [InlineKeyboardButton(text="Dashboard", callback_data="dash:home")],
            [InlineKeyboardButton(text="Settings", callback_data="settings:home")],
        ]
    )


def sports_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="NBA", callback_data="markets:nba"),
                InlineKeyboardButton(text="Football", callback_data="markets:football"),
            ],
            [
                InlineKeyboardButton(text="NFL", callback_data="markets:nfl"),
                InlineKeyboardButton(text="MLB", callback_data="markets:mlb"),
            ],
            [
                InlineKeyboardButton(text="Tennis", callback_data="markets:tennis"),
                InlineKeyboardButton(text="All Sports", callback_data="markets:all"),
            ],
            [InlineKeyboardButton(text="Back", callback_data="menu:home")],
        ]
    )


def whale_actions(address: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Current Positions", callback_data=f"whale:pos:{address}")],
            [InlineKeyboardButton(text="Recent Trades", callback_data=f"whale:trd:{address}")],
            [InlineKeyboardButton(text="Follow Whale", callback_data=f"whale:follow:{address}")],
            [InlineKeyboardButton(text="Back", callback_data="whales:top")],
        ]
    )


def alert_actions(address: str, slug: str | None = None) -> InlineKeyboardMarkup:
    rows = []
    if slug:
        rows.append([InlineKeyboardButton(text="Open Market", url=f"https://polymarket.com/event/{slug}")])
    rows.append([InlineKeyboardButton(text="Track Whale", callback_data=f"whale:follow:{address}")])
    rows.append([InlineKeyboardButton(text="Mute", callback_data=f"whale:unfollow:{address}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
