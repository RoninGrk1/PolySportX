from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from app.config.settings import settings


@lru_cache
def load_sports() -> list[dict[str, Any]]:
    path = Path(settings.sports_config_path)
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    return list(data.get("sports") or [])


def enabled_sports() -> list[dict[str, Any]]:
    return [s for s in load_sports() if s.get("enabled", True)]


def classify_sport(text: str | None, tags: list[str] | None = None) -> tuple[str | None, str | None]:
    blob = " ".join([text or ""] + [str(t) for t in (tags or [])]).lower()
    for sport in enabled_sports():
        names = [sport["id"], sport["name"], *sport.get("aliases", [])]
        if any(str(n).lower() in blob for n in names if n):
            return sport["id"], sport["name"]
    if "sport" in blob:
        return "other", "Other"
    return None, None


def sport_emoji(sport_id: str | None) -> str:
    for sport in load_sports():
        if sport["id"] == sport_id:
            return str(sport.get("emoji") or "\U0001f3df")
    return "\U0001f3df"
