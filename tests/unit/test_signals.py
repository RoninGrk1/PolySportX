from datetime import datetime, timedelta, timezone

from app.signals.clustering import ConsensusTrade, find_consensus
from app.signals.engine import SignalEngine
from app.signals.rules import SignalInputs
from app.signals.strength import HIGH, LOW, MEDIUM, VERY_HIGH, label_for


def test_signal_score_and_labels():
    engine = SignalEngine()
    low, label = engine.evaluate(SignalInputs())
    assert low == 0 and label == LOW

    mid, label = engine.evaluate(SignalInputs(large_trade=True, position_increased=True))
    assert mid == 35 and label == LOW

    high, label = engine.evaluate(
        SignalInputs(
            large_trade=True,
            whale_score=85,
            sports_specialist=True,
            position_increased=True,
        )
    )
    assert high == 70 and label == HIGH

    very, label = engine.evaluate(
        SignalInputs(
            large_trade=True,
            whale_score=90,
            sports_specialist=True,
            position_increased=True,
            multiple_whales_agree=True,
            unusual_trade_size=True,
        )
    )
    assert very == 100 and label == VERY_HIGH
    assert label_for(45) == MEDIUM


def test_multi_whale_consensus():
    now = datetime.now(timezone.utc)
    trades = [
        ConsensusTrade(1, 10, "YES", 20_000, now),
        ConsensusTrade(2, 10, "YES", 14_000, now + timedelta(minutes=3)),
        ConsensusTrade(3, 10, "YES", 31_000, now + timedelta(minutes=8)),
        ConsensusTrade(4, 10, "NO", 50_000, now),
    ]
    hits = find_consensus(trades, window_seconds=900, min_whales=3)
    assert any(h.count == 3 and abs(h.combined_notional - 65_000) < 1 for h in hits)
    none = find_consensus(trades, window_seconds=60, min_whales=3)
    assert none == []
