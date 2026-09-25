from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.common import main_menu

router = Router()


@router.callback_query(F.data == "alerts:home")
async def cb_alerts(query: CallbackQuery) -> None:
    await query.message.edit_text(
        "Whale Alerts\n"
        "You will receive alerts for large trades, new positions, exits, "
        "and multi-whale consensus based on your settings.\n\n"
        "Alerts describe observed activity -- not guaranteed outcomes.",
        reply_markup=main_menu(),
    )
    await query.answer()
