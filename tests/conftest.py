import pytest


@pytest.fixture
def raw_market():
    return {
        "conditionId": "0xabc123",
        "question": "Lakers vs Celtics",
        "slug": "lakers-vs-celtics",
        "active": True,
        "closed": False,
        "clobTokenIds": '["tokyes","tokno"]',
        "outcomePrices": '["0.58","0.42"]',
        "volumeNum": 125000,
        "volume24hr": 18000,
        "liquidityNum": 42000,
        "endDate": "2026-10-01T00:00:00Z",
        "tags": [{"label": "NBA"}, {"label": "Sports"}],
        "eventId": "555",
    }


@pytest.fixture
def raw_trade():
    return {
        "proxyWallet": "0x8F1111111111111111111111111111111111121A",
        "side": "BUY",
        "asset": "tokyes",
        "conditionId": "0xabc123",
        "size": 48000,
        "price": 0.58,
        "timestamp": 1710000000,
        "outcome": "Yes",
        "transactionHash": "0xdeadbeef",
        "title": "Lakers vs Celtics",
        "slug": "lakers-vs-celtics",
    }
