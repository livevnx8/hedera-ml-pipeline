"""
Risk management for live trading.
Provides stop-loss, take-profit, daily loss limits, and position caps.
"""

from typing import Optional


class RiskManagement:
    """
    Trading risk management with configurable limits.

    Features:
    - Stop-loss and take-profit price calculation
    - Maximum daily loss limit
    - Maximum concurrent positions
    - Daily P&L tracking
    """

    def __init__(
        self,
        stop_loss_pct: float = 0.01,
        take_profit_pct: float = 0.02,
        max_daily_loss_pct: float = 0.05,
        max_positions: int = 5,
    ):
        """
        Args:
            stop_loss_pct: Stop loss as fraction of entry price (default 1%).
            take_profit_pct: Take profit as fraction of entry price (default 2%).
            max_daily_loss_pct: Maximum daily loss as fraction of portfolio (default 5%).
            max_positions: Maximum concurrent open positions (default 5).
        """
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_positions = max_positions

        self.daily_pnl: float = 0.0
        self.position_count: int = 0

    # ── Position Gating ────────────────────────────────────────────────

    def should_open_position(self) -> bool:
        """Check if a new position can be opened."""
        if self.daily_pnl < -self.max_daily_loss_pct:
            return False
        if self.position_count >= self.max_positions:
            return False
        return True

    # ── Price Calculations ─────────────────────────────────────────────

    def calculate_stop_loss(
        self, entry_price: float, direction: str = "long"
    ) -> float:
        """
        Calculate stop loss price.

        Args:
            entry_price: Position entry price.
            direction: 'long' or 'short'.

        Returns:
            Stop loss trigger price.
        """
        if direction == "long":
            return entry_price * (1 - self.stop_loss_pct)
        return entry_price * (1 + self.stop_loss_pct)

    def calculate_take_profit(
        self, entry_price: float, direction: str = "long"
    ) -> float:
        """
        Calculate take profit price.

        Args:
            entry_price: Position entry price.
            direction: 'long' or 'short'.

        Returns:
            Take profit trigger price.
        """
        if direction == "long":
            return entry_price * (1 + self.take_profit_pct)
        return entry_price * (1 - self.take_profit_pct)

    # ── State Management ───────────────────────────────────────────────

    def update_pnl(self, pnl: float):
        """Update cumulative daily P&L."""
        self.daily_pnl += pnl

    def increment_position_count(self):
        """Record a new position opened."""
        self.position_count += 1

    def decrement_position_count(self):
        """Record a position closed."""
        self.position_count = max(0, self.position_count - 1)

    def reset_daily(self):
        """Reset daily metrics (call at start of trading day)."""
        self.daily_pnl = 0.0
        self.position_count = 0
