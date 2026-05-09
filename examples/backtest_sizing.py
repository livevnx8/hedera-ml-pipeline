#!/usr/bin/env python3
"""
Simple backtesting example for position sizing strategies.

This example shows how to evaluate Kelly Criterion and fixed-fraction
position sizing using historical price data.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hedera_ml_pipeline import KellyCriterionSizing, FixedFractionSizing


def backtest_kelly(prices: list[float], confidences: list[float], portfolio_value: float):
    """Backtest Kelly Criterion sizing over a price series."""
    sizing = KellyCriterionSizing(max_fraction=0.02)
    results = []

    for price, confidence in zip(prices, confidences):
        position = sizing.calculate(portfolio_value, price, confidence)
        results.append({
            "price": price,
            "confidence": confidence,
            "position_size": position.size,
            "fraction": position.fraction,
            "risk_amount": position.risk_amount,
        })

    return results


def backtest_fixed_fraction(prices: list[float], portfolio_value: float, fraction: float):
    """Backtest fixed-fraction sizing over a price series."""
    sizing = FixedFractionSizing(fraction=fraction)
    results = []

    for price in prices:
        position = sizing.calculate(portfolio_value, price)
        results.append({
            "price": price,
            "position_size": position.size,
            "fraction": position.fraction,
        })

    return results


if __name__ == "__main__":
    # Example historical price data (HBAR)
    prices = [0.28, 0.29, 0.30, 0.31, 0.30, 0.29, 0.28, 0.27, 0.28, 0.30]
    confidences = [0.55, 0.60, 0.65, 0.70, 0.55, 0.50, 0.45, 0.55, 0.60, 0.65]
    portfolio_value = 10_000

    print("=== Kelly Criterion Backtest ===")
    kelly_results = backtest_kelly(prices, confidences, portfolio_value)
    for r in kelly_results:
        print(f"Price: ${r['price']:.2f} | Confidence: {r['confidence']:.2f} | Size: {r['position_size']:.2f} HBAR | Fraction: {r['fraction']:.3f}")

    print("\n=== Fixed-Fraction Backtest (2%) ===")
    fixed_results = backtest_fixed_fraction(prices, portfolio_value, 0.02)
    for r in fixed_results:
        print(f"Price: ${r['price']:.2f} | Size: {r['position_size']:.2f} HBAR | Fraction: {r['fraction']:.3f}")
