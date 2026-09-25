from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.common import sports_menu
from app.bot.messages.templates import market_card
from app.db.database import SessionLocal
from app.services.market_service import MarketService

router = Router()


async def _render(sport: str | None) -> str:
    async with SessionLocal() as session:
        rows = await MarketService(session).list_markets(sport=None if sport == "all" else sport, limit=8)
    if not rows:
        return "No sports markets synced yet. The market worker is still catching up."
    return "\n\n".join(market_card(m) for m in rows)


@router.message(Command("markets"))
async def cmd_markets(message: Message) -> None:
    await message.answer(await _render("all"), reply_markup=sports_menu())


@router.callback_query(F.data.startswith("markets:"))
async def cb_markets(query: CallbackQuery) -> None:
    sport = query.data.split(":", 1)[1]
    await query.message.edit_text(await _render(sport), reply_markup=sports_menu())
    await query.answer()
