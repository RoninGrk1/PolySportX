from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.common import main_menu, whale_actions
from app.bot.messages.templates import top5_card, whale_card
from app.db.database import SessionLocal
from app.db.repositories.wallets import WalletRepository
from app.services.user_service import UserService
from app.services.whale_service import WhaleService

router = Router()


async def _top_text() -> str:
    async with SessionLocal() as session:
        svc = WhaleService(session)
        snaps = await svc.top()
        rows = []
        for snap in snaps:
            wallet = await WalletRepository(session).get_by_id(snap.wallet_id)
            if wallet:
                rows.append((snap.rank, wallet))
        if not rows:
            whales = await svc.list_whales(limit=5)
            rows = [(i, w) for i, w in enumerate(whales, start=1)]
    return top5_card(rows)


@router.message(Command("top5"))
async def cmd_top5(message: Message) -> None:
    await message.answer(await _top_text(), reply_markup=main_menu())


@router.callback_query(F.data == "whales:top")
async def cb_top5(query: CallbackQuery) -> None:
    await query.message.edit_text(await _top_text(), reply_markup=main_menu())
    await query.answer()


@router.message(Command("whale"))
async def cmd_whale(message: Message) -> None:
    parts = (message.text or "").split()
    if len(parts) < 2:
        await message.answer("Usage: /whale 0x...")
        return
    address = parts[1]
    async with SessionLocal() as session:
        wallet = await WhaleService(session).by_address(address)
    if wallet is None:
        await message.answer("Wallet not tracked yet.")
        return
    await message.answer(whale_card(wallet), reply_markup=whale_actions(wallet.address))


@router.message(Command("follow"))
async def cmd_follow(message: Message) -> None:
    parts = (message.text or "").split()
    if len(parts) < 2:
        await message.answer("Usage: /follow 0x...")
        return
    async with SessionLocal() as session:
        await UserService(session).follow_address(message.from_user.id, parts[1])
    await message.answer(f"Now following {parts[1]}")


@router.message(Command("unfollow"))
async def cmd_unfollow(message: Message) -> None:
    parts = (message.text or "").split()
    if len(parts) < 2:
        await message.answer("Usage: /unfollow 0x...")
        return
    async with SessionLocal() as session:
        ok = await UserService(session).unfollow_address(message.from_user.id, parts[1])
    await message.answer("Unfollowed." if ok else "That wallet was not on your list.")


@router.callback_query(F.data.startswith("whale:follow:"))
async def cb_follow(query: CallbackQuery) -> None:
    address = query.data.split(":", 2)[2]
    async with SessionLocal() as session:
        await UserService(session).follow_address(query.from_user.id, address)
    await query.answer("Following")


@router.callback_query(F.data.startswith("whale:unfollow:"))
async def cb_unfollow(query: CallbackQuery) -> None:
    address = query.data.split(":", 2)[2]
    async with SessionLocal() as session:
        await UserService(session).unfollow_address(query.from_user.id, address)
    await query.answer("Muted")
