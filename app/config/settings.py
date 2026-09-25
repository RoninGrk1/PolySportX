from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "PolySportX"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/polysportx"
    redis_url: str = "redis://localhost:6379/0"

    telegram_bot_token: str = ""
    telegram_admin_ids: str = ""

    polymarket_gamma_url: str = "https://gamma-api.polymarket.com"
    polymarket_clob_url: str = "https://clob.polymarket.com"
    polymarket_data_url: str = "https://data-api.polymarket.com"

    admin_api_key: str = "change-me"
    sentry_dsn: str = ""

    whale_min_volume: float = 10_000
    whale_min_trades: int = 20
    whale_min_active_days: int = 7
    whale_min_sports_exposure: float = 0.40

    global_min_notional: float = 5_000
    whale_size_multiplier: float = 3.0

    consensus_window_seconds: int = 900
    alert_dedupe_ttl_seconds: int = 900
    top5_refresh_seconds: int = 300
    market_sync_seconds: int = 120
    trade_poll_seconds: int = 15
    reconcile_seconds: int = 900
    http_timeout_seconds: float = 20.0

    score_weight_roi: float = 0.30
    score_weight_pnl: float = 0.25
    score_weight_recent: float = 0.15
    score_weight_consistency: float = 0.10
    score_weight_activity: float = 0.10
    score_weight_timing: float = 0.10

    sports_config_path: str = "sports.yaml"

    @property
    def admin_ids(self) -> list[int]:
        if not self.telegram_admin_ids.strip():
            return []
        return [int(x) for x in self.telegram_admin_ids.split(",") if x.strip()]

    @property
    def is_dev(self) -> bool:
        return self.app_env.lower() in {"dev", "development", "local"}


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
