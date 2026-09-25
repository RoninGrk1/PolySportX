import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.middleware.user import UserMiddleware
from app.bot.routers import alerts, markets, settings, start, whales
from app.config.logging import setup_logging
from app.config.settings import settings
from app.db.database import init_db

logger = logging.getLogger(__name__)


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.update.middleware(UserMiddleware())
    dp.include_router(start.router)
    dp.include_router(markets.router)
    dp.include_router(whales.router)
    dp.include_router(alerts.router)
    dp.include_router(settings.router)
    return dp


async def run() -> None:
    setup_logging()
    if not settings.telegram_bot_token:
        logger.error("TELEGRAM_BOT_TOKEN is not set")
        return
    try:
        await init_db()
    except Exception:
        logger.exception("database init failed")
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = build_dispatcher()
    logger.info("starting PolySportX bot")
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
