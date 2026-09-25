from __future__ import annotations

from datetime import datetime, timezone


def alert_key(wallet: str | int, market: str | int, event_type: str, bucket_seconds: int = 900) -> str:
    now = int(datetime.now(timezone.utc).timestamp())
    bucket = now - (now % bucket_seconds)
    return f"alert:{wallet}:{market}:{event_type}:{bucket}"


class AlertDedupe:
    def __init__(self, redis=None, ttl: int = 900):
        self.redis = redis
        self.ttl = ttl
        self._memory: dict[str, str] = {}

    async def should_send(self, key: str) -> bool:
        if self.redis is not None:
            exists = await self.redis.exists(key)
            if exists:
                return False
            await self.redis.setex(key, self.ttl, "1")
            return True
        if key in self._memory:
            return False
        self._memory[key] = "1"
        return True
