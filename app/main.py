from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.api.routes import admin, alerts, health, markets, signals, whales
from app.config.logging import setup_logging
from app.config.settings import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    try:
        await init_db()
    except Exception:
        pass
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(health.router)
app.include_router(markets.router)
app.include_router(whales.router)
app.include_router(alerts.router)
app.include_router(signals.router)
app.include_router(admin.router)


@app.get("/metrics")
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
