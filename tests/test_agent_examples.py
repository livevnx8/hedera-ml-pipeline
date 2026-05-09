import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from examples.network_health_agent import build_health_report
from examples.risk_gate_agent import run_risk_gate


def test_network_health_agent_reports_healthy_sample():
    metrics = {
        "staking": {"stake_total": 1_000_000},
        "supply": {"released_supply": 10_000_000, "total_supply": 50_000_000, "circulation_pct": 20.0},
        "transactions": {"total_transactions": 100, "unique_accounts": 25},
    }

    report = build_health_report(metrics)

    assert report["agent"] == "network_health_agent"
    assert report["status"] == "healthy"
    assert report["score"] == 100
    assert report["watch_items"] == []


def test_risk_gate_agent_blocks_daily_loss():
    report = run_risk_gate(
        portfolio_value=10_000,
        hbar_price=0.30,
        confidence=0.52,
        daily_pnl=-0.06,
        open_positions=1,
    )

    assert report["agent"] == "risk_gate_agent"
    assert report["decision"] == "block"
    assert "daily loss" in report["reason"]
