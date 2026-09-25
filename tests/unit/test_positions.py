from app.whale.positions import (
    FULL_EXIT,
    NEW_POSITION,
    PARTIAL_EXIT,
    POSITION_INCREASE,
    apply_trade,
    detect_event,
    is_large_trade,
)


def test_new_position_and_increase():
    first = apply_trade(0, None, 0, "BUY", 0.50, 100)
    assert first.size == 100
    assert first.average_entry == 0.50
    event = detect_event(0, first.size)
    assert event == NEW_POSITION

    second = apply_trade(first.size, first.average_entry, first.realized_pnl, "BUY", 0.60, 100)
    assert second.size == 200
    assert abs(second.average_entry - 0.55) < 1e-9
    assert detect_event(first.size, second.size) == POSITION_INCREASE


def test_partial_and_full_exit_realizes_pnl():
    opened = apply_trade(0, None, 0, "BUY", 0.40, 100)
    partial = apply_trade(opened.size, opened.average_entry, opened.realized_pnl, "SELL", 0.60, 40)
    assert partial.size == 60
    assert abs(partial.realized_pnl - 8.0) < 1e-9
    assert detect_event(opened.size, partial.size, "SELL") == PARTIAL_EXIT

    closed = apply_trade(partial.size, partial.average_entry, partial.realized_pnl, "SELL", 0.70, 60)
    assert closed.size == 0
    assert detect_event(partial.size, closed.size) == FULL_EXIT
    assert abs(closed.realized_pnl - (8.0 + 18.0)) < 1e-9


def test_large_trade_absolute_and_relative():
    assert is_large_trade(6000, 100, 5000, 3) is True
    assert is_large_trade(400, 100, 5000, 3) is True
    assert is_large_trade(200, 100, 5000, 3) is False
