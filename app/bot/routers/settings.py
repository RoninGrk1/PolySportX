from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.db.database import SessionLocal
from app.db.repositories.users import UserRepository

router = Router()


def settings_kb(user) -> InlineKeyboardMarkup:
    def mark(flag: bool, label: str) -> str:
        return f"{'[x]' if flag else '[ ]'} {label}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=mark(user.alert_large_trades, "Large trades"), callback_data="set:large")],
            [InlineKeyboardButton(text=mark(user.alert_entries, "New positions"), callback_data="set:entries")],
            [InlineKeyboardButton(text=mark(user.alert_exits, "Whale exits"), callback_data="set:exits")],
            [InlineKeyboardButton(text=mark(user.alert_consensus, "Multi-whale consensus"), callback_data="set:consensus")],
            [InlineKeyboardButton(text=mark(user.alert_top5, "Top-5 changes"), callback_data="set:top5")],
            [InlineKeyboardButton(text="Back", callback_data="menu:home")],
        ]
    )


async def _user(telegram_id: int):
    async with SessionLocal() as session:
        repo = UserRepository(session)
        user = await repo.upsert(telegram_id)
        await session.commit()
        return user


@router.message(Command("settings"))
async def cmd_settings(message: Message) -> None:
    user = await _user(message.from_user.id)
    await message.answer("Alert preferences", reply_markup=settings_kb(user))


@router.callback_query(F.data == "settings:home")
async def cb_settings(query: CallbackQuery) -> None:
    user = await _user(query.from_user.id)
    await query.message.edit_text("Alert preferences", reply_markup=settings_kb(user))
    await query.answer()


@router.callback_query(F.data.startswith("set:"))
async def cb_toggle(query: CallbackQuery) -> None:
    field = {
        "large": "alert_large_trades",
        "entries": "alert_entries",
        "exits": "alert_exits",
        "consensus": "alert_consensus",
        "top5": "alert_top5",
    }[query.data.split(":")[1]]
    async with SessionLocal() as session:
        repo = UserRepository(session)
        user = await repo.upsert(query.from_user.id)
        setattr(user, field, not bool(getattr(user, field)))
        await session.commit()
        await session.refresh(user)
    await query.message.edit_reply_markup(reply_markup=settings_kb(user))
    await query.answer("Updated")
