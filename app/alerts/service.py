import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.alerts.dedupe import AlertDedupe, alert_key
from app.alerts.templates import consensus_alert, whale_alert
from app.config.settings import settings
from app.db.models.alert import Alert
from app.db.repositories.alerts import AlertRepository
from app.db.repositories.users import UserRepository
from app.observability.metrics import alerts_failed, alerts_sent

logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self, session: AsyncSession, redis=None, bot=None):
        self.session = session
        self.bot = bot
        self.dedupe = AlertDedupe(redis, ttl=settings.alert_dedupe_ttl_seconds)
        self.alerts = AlertRepository(session)
        self.users = UserRepository(session)

    async def emit_whale_move(self, payload: dict) -> int:
        key = alert_key(
            payload.get("wallet_id") or payload.get("address"),
            payload.get("market_id") or payload.get("condition_id"),
            payload.get("event_type") or "WHALE_MOVE",
            settings.alert_dedupe_ttl_seconds,
        )
        if not await self.dedupe.should_send(key):
            return 0
        text = whale_alert(
            sport=payload.get("sport"),
            question=payload.get("question") or "Market",
            address=payload.get("address") or "",
            side=payload.get("side") or "BUY",
            outcome=payload.get("outcome") or "YES",
            size=float(payload.get("notional") or 0),
            entry=float(payload.get("price") or 0),
            current=payload.get("current_price"),
            position=float(payload.get("position") or payload.get("notional") or 0),
            roi=float(payload.get("roi") or 0),
            strength=payload.get("strength") or "MEDIUM",
        )
        return await self._fanout(text, payload, alert_type=payload.get("event_type") or "WHALE_MOVE")

    async def emit_consensus(self, payload: dict) -> int:
        key = alert_key("consensus", payload.get("market_id"), payload.get("outcome"), settings.alert_dedupe_ttl_seconds)
        if not await self.dedupe.should_send(key):
            return 0
        text = consensus_alert(
            question=payload.get("question") or "Market",
            count=int(payload.get("count") or 0),
            notional=float(payload.get("combined_notional") or 0),
            outcome=payload.get("outcome") or "YES",
        )
        return await self._fanout(text, payload, alert_type="CONSENSUS")

    async def _fanout(self, text: str, payload: dict, alert_type: str) -> int:
        users = await self.users.all_alert_users()
        sent = 0
        for user in users:
            if not self._user_wants(user, payload, alert_type):
                continue
            try:
                if self.bot is not None:
                    await self.bot.send_message(chat_id=user.telegram_id, text=text)
                await self.alerts.add_alert(
                    Alert(
                        user_id=user.id,
                        wallet_id=payload.get("wallet_id"),
                        market_id=payload.get("market_id"),
                        alert_type=alert_type,
                        signal_strength=payload.get("strength"),
                        payload=payload,
                    )
                )
                alerts_sent.inc()
                sent += 1
            except Exception:
                logger.exception("failed to send alert to %s", user.telegram_id)
                alerts_failed.inc()
        await self.session.commit()
        return sent

    def _user_wants(self, user, payload: dict, alert_type: str) -> bool:
        notional = float(payload.get("notional") or payload.get("combined_notional") or 0)
        if float(user.min_trade_notional or 0) and notional < float(user.min_trade_notional):
            if alert_type != "CONSENSUS":
                return False
        sport = payload.get("sport")
        if user.sports_filter and sport and sport not in user.sports_filter:
            return False
        if alert_type in {"NEW_POSITION", "POSITION_INCREASE"} and not user.alert_entries:
            return False
        if alert_type in {"FULL_EXIT", "PARTIAL_EXIT", "POSITION_DECREASE"} and not user.alert_exits:
            return False
        if alert_type == "CONSENSUS" and not user.alert_consensus:
            return False
        if payload.get("large_trade") and not user.alert_large_trades:
            return False
        return True
