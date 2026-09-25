from functools import lru_cache

import redis.asyncio as redis

from app.config.settings import settings


@lru_cache
def get_redis() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)


STREAM_TRADES = "stream:trades"
STREAM_POSITIONS = "stream:positions"
STREAM_SIGNALS = "stream:signals"
CHANNEL_TRADE_CREATED = "trade.created"
CHANNEL_POSITION_CHANGED = "position.changed"
CHANNEL_SIGNAL_CREATED = "signal.created"
