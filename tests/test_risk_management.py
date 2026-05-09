from src.risk_management import RiskManagement


def test_risk_gate_allows_default_state():
    risk = RiskManagement(max_daily_loss_pct=0.05, max_positions=5)

    assert risk.should_open_position() is True


def test_risk_gate_blocks_daily_loss():
    risk = RiskManagement(max_daily_loss_pct=0.05)
    risk.update_pnl(-0.06)

    assert risk.should_open_position() is False


def test_risk_gate_blocks_max_positions():
    risk = RiskManagement(max_positions=1)
    risk.increment_position_count()

    assert risk.should_open_position() is False


def test_stop_loss_and_take_profit_for_long():
    risk = RiskManagement(stop_loss_pct=0.01, take_profit_pct=0.02)

    assert risk.calculate_stop_loss(1.00, "long") == 0.99
    assert risk.calculate_take_profit(1.00, "long") == 1.02
