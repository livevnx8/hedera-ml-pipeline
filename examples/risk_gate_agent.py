#!/usr/bin/env python3
"""
Risk gate agent example.

Shows how an agent can convert signal confidence into a proposed HBAR position,
then pass that proposal through explicit risk controls before execution.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.position_sizing import KellyCriterionSizing
from src.risk_management import RiskManagement


def run_risk_gate(
    portfolio_value: float,
    hbar_price: float,
    confidence: float,
    daily_pnl: float = 0.0,
    open_positions: int = 0,
) -> dict:
    sizing = KellyCriterionSizing()
    risk = RiskManagement(
        stop_loss_pct=0.01,
        take_profit_pct=0.02,
        max_daily_loss_pct=0.05,
        max_positions=5,
    )

    risk.daily_pnl = daily_pnl
    risk.position_count = open_positions

    position = sizing.calculate(
        portfolio_value=portfolio_value,
        current_price=hbar_price,
        confidence=confidence,
    )

    allowed = risk.should_open_position()
    reason = "allowed"
    if risk.daily_pnl < -risk.max_daily_loss_pct:
        reason = "blocked: daily loss limit reached"
    elif risk.position_count >= risk.max_positions:
        reason = "blocked: maximum open positions reached"

    return {
        "agent": "risk_gate_agent",
        "decision": "allow" if allowed else "block",
        "reason": reason,
        "inputs": {
            "portfolio_value": portfolio_value,
            "hbar_price": hbar_price,
            "confidence": confidence,
            "daily_pnl": daily_pnl,
            "open_positions": open_positions,
        },
        "proposal": {
            "position_size_hbar": round(position.size, 4),
            "portfolio_fraction": round(position.fraction, 6),
            "risk_amount": round(position.risk_amount, 4),
            "stop_loss": round(risk.calculate_stop_loss(hbar_price, "long"), 6),
            "take_profit": round(risk.calculate_take_profit(hbar_price, "long"), 6),
        },
    }


def main() -> None:
    report = run_risk_gate(
        portfolio_value=10_000,
        hbar_price=0.30,
        confidence=0.52,
        daily_pnl=0.0,
        open_positions=1,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
