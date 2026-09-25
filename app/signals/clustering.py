from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ConsensusTrade:
    wallet_id: int
    market_id: int
    outcome: str
    notional: float
    timestamp: datetime
    whale_score: float = 0.0


@dataclass
class Consensus:
    market_id: int
    outcome: str
    wallet_ids: list[int]
    combined_notional: float
    count: int


def find_consensus(trades: list[ConsensusTrade], window_seconds: int = 900, min_whales: int = 2) -> list[Consensus]:
    groups: dict[tuple[int, str], list[ConsensusTrade]] = defaultdict(list)
    for trade in trades:
        groups[(trade.market_id, trade.outcome)].append(trade)

    results: list[Consensus] = []
    window = timedelta(seconds=window_seconds)
    for (market_id, outcome), bucket in groups.items():
        bucket.sort(key=lambda t: t.timestamp)
        for i, anchor in enumerate(bucket):
            cluster = [anchor]
            seen = {anchor.wallet_id}
            for other in bucket[i + 1 :]:
                if other.timestamp - anchor.timestamp > window:
                    break
                if other.wallet_id in seen:
                    continue
                seen.add(other.wallet_id)
                cluster.append(other)
            if len(seen) >= min_whales:
                results.append(
                    Consensus(
                        market_id=market_id,
                        outcome=outcome,
                        wallet_ids=sorted(seen),
                        combined_notional=sum(t.notional for t in cluster),
                        count=len(seen),
                    )
                )
    unique: dict[tuple, Consensus] = {}
    for item in results:
        key = (item.market_id, item.outcome, tuple(item.wallet_ids))
        prev = unique.get(key)
        if prev is None or item.combined_notional > prev.combined_notional:
            unique[key] = item
    return list(unique.values())
