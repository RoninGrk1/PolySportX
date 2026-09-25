# PolySportX

Telegram-native Polymarket sports analytics, whale tracking, and copy-trade **signal scanner**.

Bot: [@PolySportX_Bot](https://t.me/PolySportX_Bot)

The MVP is an analytics and alerting platform. It does **not** execute trades, take custody of funds, or ask for private keys.

PolySportX answers three questions quickly:

1. **WHAT** is happening?
2. **WHICH** whale is doing it?
3. **IS** this unusual or significant?

## Features

- Sports market discovery with live prices, volume, and liquidity
- Wallet discovery and whale ranking (never by raw P&L alone)
- Position reconstruction and entry/exit detection
- Large-trade detection (absolute + relative to the wallet)
- Multi-whale consensus signals
- Telegram alerts with Redis deduplication
- User watchlists and alert preferences
- FastAPI internal API + Docker Compose workers

## Quick start

```bash
cp .env.example .env
# set TELEGRAM_BOT_TOKEN and ADMIN_API_KEY

docker compose up --build
```

API health check: `http://localhost:8000/health`

```bash
pip install -e ".[dev]"
pytest -q
```
