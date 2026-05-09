"""
Position sizing strategies for risk-managed trading.
Implements Kelly Criterion and Fixed Fraction approaches.
"""

import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class PositionSize:
    """Result of a position sizing calculation."""

    size: float
    """Position size in base currency (e.g., HBAR)."""

    fraction: float
    """Fraction of portfolio allocated (0.0 - 1.0)."""

    confidence: float
    """Model confidence used in calculation (0.0 - 1.0)."""

    risk_amount: float
    """Amount at risk in quote currency (e.g., USD)."""


class KellyCriterionSizing:
    """
    Kelly Criterion position sizing.

    Optimizes long-term growth by sizing positions based on edge and variance.

    Formula:
        f* = (b * p - q) / b

    Where:
        f* = optimal fraction of portfolio
        b  = win/loss ratio (odds)
        p  = probability of winning
        q  = probability of losing (1 - p)

    Uses half-Kelly (f*/2) by default for reduced volatility.
    """

    def __init__(
        self,
        base_win_rate: float = 0.52,
        avg_win: float = 1.0,
        avg_loss: float = 1.0,
        max_fraction: float = 0.02,
        kelly_fraction: float = 0.5,
    ):
        """
        Args:
            base_win_rate: Expected win rate from backtesting (default 0.52).
            avg_win: Average win as multiple of risk (default 1.0).
            avg_loss: Average loss as multiple of risk (default 1.0).
            max_fraction: Maximum portfolio fraction per trade (default 2%).
            kelly_fraction: Fraction of full Kelly to use (0.5 = half-Kelly).
        """
        self.base_win_rate = base_win_rate
        self.avg_win = avg_win
        self.avg_loss = avg_loss
        self.max_fraction = max_fraction
        self.kelly_fraction = kelly_fraction

    def calculate(
        self,
        portfolio_value: float,
        current_price: float,
        confidence: float = 0.5,
        win_rate_override: Optional[float] = None,
    ) -> PositionSize:
        """
        Calculate position size using Kelly Criterion.

        Args:
            portfolio_value: Total portfolio value in quote currency.
            current_price: Current asset price in quote currency.
            confidence: Model confidence (0-1). Higher = larger position.
            win_rate_override: Override base win rate if known.

        Returns:
            PositionSize with calculated size, fraction, and risk.
        """
        p = win_rate_override if win_rate_override is not None else self.base_win_rate

        # Adjust win rate based on model confidence (±10%)
        adjusted_p = p + (confidence - 0.5) * 0.2
        adjusted_p = max(0.51, min(0.60, adjusted_p))

        q = 1 - adjusted_p
        b = self.avg_win / self.avg_loss

        # Kelly formula
        kelly_f = (b * adjusted_p - q) / b
        kelly_f *= self.kelly_fraction  # Half-Kelly

        fraction = min(kelly_f, self.max_fraction)
        fraction = max(0.001, fraction)  # Minimum 0.1%

        position_value = portfolio_value * fraction
        size = position_value / current_price
        risk_amount = position_value * self.avg_loss / (self.avg_win + self.avg_loss)

        return PositionSize(
            size=size,
            fraction=fraction,
            confidence=confidence,
            risk_amount=risk_amount,
        )


class FixedFractionSizing:
    """
    Fixed fraction position sizing.

    Simpler approach: allocate a fixed percentage of portfolio per trade,
    adjusted by model confidence.
    """

    def __init__(
        self,
        base_fraction: float = 0.01,
        max_fraction: float = 0.02,
        min_fraction: float = 0.005,
    ):
        """
        Args:
            base_fraction: Base allocation at 50% confidence (default 1%).
            max_fraction: Maximum allocation at 100% confidence (default 2%).
            min_fraction: Minimum allocation at 0% confidence (default 0.5%).
        """
        self.base_fraction = base_fraction
        self.max_fraction = max_fraction
        self.min_fraction = min_fraction

    def calculate(
        self,
        portfolio_value: float,
        current_price: float,
        confidence: float = 0.5,
    ) -> PositionSize:
        """
        Calculate position size using fixed fraction.

        Args:
            portfolio_value: Total portfolio value in quote currency.
            current_price: Current asset price in quote currency.
            confidence: Model confidence (0-1).

        Returns:
            PositionSize with calculated size, fraction, and risk.
        """
        if confidence >= 0.5:
            fraction = self.base_fraction + (confidence - 0.5) * (
                self.max_fraction - self.base_fraction
            ) * 2
        else:
            fraction = self.base_fraction - (0.5 - confidence) * (
                self.base_fraction - self.min_fraction
            ) * 2

        fraction = max(self.min_fraction, min(self.max_fraction, fraction))

        position_value = portfolio_value * fraction
        size = position_value / current_price
        risk_amount = position_value * 0.01  # Assume 1% stop loss

        return PositionSize(
            size=size,
            fraction=fraction,
            confidence=confidence,
            risk_amount=risk_amount,
        )
