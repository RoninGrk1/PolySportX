from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.common import main_menu
from app.bot.messages.templates import START

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(START, reply_markup=main_menu())


@router.callback_query(F.data == "menu:home")
async def cb_home(query: CallbackQuery) -> None:
    await query.message.edit_text(START, reply_markup=main_menu())
    await query.answer()


@router.callback_query(F.data == "dash:home")
async def cb_dash(query: CallbackQuery) -> None:
    await query.message.edit_text(
        "Dashboard\nWatchlist and recent alerts live here once you follow a whale.",
        reply_markup=main_menu(),
    )
    await query.answer()
