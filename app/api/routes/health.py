from fastapi import APIRouter

from app.config.settings import settings
from app.db.database import get_engine
from app.polymarket.client import PolymarketClient

router = APIRouter()


@router.get("/health")
async def health():
    status = {
        "status": "ok",
        "database": "ok",
        "redis": "ok",
        "polymarket": "ok",
        "telegram": "ok" if settings.telegram_bot_token else "unconfigured",
    }
    try:
        async with get_engine().connect() as conn:
            await conn.exec_driver_sql("SELECT 1")
    except Exception:
        status["database"] = "error"
        status["status"] = "degraded"
    try:
        import redis.asyncio as redis

        client = redis.from_url(settings.redis_url)
        await client.ping()
        await client.aclose()
    except Exception:
        status["redis"] = "error"
        status["status"] = "degraded"
    try:
        ok = await PolymarketClient().ping()
        if not ok:
            status["polymarket"] = "error"
            status["status"] = "degraded"
    except Exception:
        status["polymarket"] = "error"
        status["status"] = "degraded"
    return status
