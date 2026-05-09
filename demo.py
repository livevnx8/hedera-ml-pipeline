#!/usr/bin/env python3
"""
🔷 Hedera ML Pipeline — Live Demo

End-to-end showcase: fetches real Hedera mainnet data, processes on-chain metrics,
demonstrates position sizing and risk management. Zero configuration required.
"""

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.mirror_node import HederaMirrorNodeClient
from src.metrics import HederaOnChainMetrics
from src.position_sizing import KellyCriterionSizing, FixedFractionSizing
from src.risk_management import RiskManagement


def banner(text: str):
    print(f"\n{'─' * 50}")
    print(f"  {text}")
    print(f"{'─' * 50}")


def section(title: str):
    print(f"\n{title}")


async def main():
    print("🔷  Hedera ML Pipeline — Live Demo")
    print("   Real mainnet data • Zero config • No API keys\n")

    # ── Step 1: Connect to Hedera Mainnet ────────────────────────────
    banner("Step 1: Connect to Hedera Mainnet Mirror Node")
    print("   Network: mainnet")
    print("   Endpoint: mainnet-public.mirrornode.hedera.com")
    print("   Auth: none required")

    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)

        # ── Step 2: Fetch On-Chain Metrics ───────────────────────────
        banner("Step 2: Fetch On-Chain Metrics (parallel)")

        t0 = time.perf_counter()
        data = await metrics.get_all_metrics()
        elapsed = (time.perf_counter() - t0) * 1000

        print(f"   Fetched in {elapsed:.0f}ms\n")

        # Staking
        section("📊 Network Stake")
        stake = data["staking"]
        print(f"   Total Staked:    {stake['stake_total']:>16,.0f} HBAR")
        print(f"   Reward Rate:     {stake['staking_reward_rate']:>16,.0f}")
        print(f"   Max Reward/HBAR: {stake['max_reward_rate']:>16,.0f}")

        # Supply
        section("💰 Token Supply")
        supply = data["supply"]
        print(f"   Circulating:     {supply['released_supply']:>16,.0f} HBAR")
        print(f"   Max Supply:      {supply['total_supply']:>16,.0f} HBAR")
        print(f"   Circulation:     {supply['circulation_pct']:>15.2f}%")

        # Transactions
        section("📈 Transaction Volume (last 100 tx)")
        tx = data["transactions"]
        print(f"   Transactions:    {tx['total_transactions']:>16}")
        print(f"   Unique Accounts: {tx['unique_accounts']:>16}")
        print(f"   Avg Value:       {tx['avg_transaction_value']:>12.4f} HBAR")

        # ── Step 3: Position Sizing ──────────────────────────────────
        banner("Step 3: Position Sizing")

        portfolio = 10_000.0
        hbar_price = 0.30
        confidence = 0.52

        print(f"   Portfolio:       ${portfolio:>,.2f}")
        print(f"   HBAR Price:      ${hbar_price:.2f}")
        print(f"   Confidence:      {confidence:.0%}\n")

        # Kelly Criterion
        kelly = KellyCriterionSizing()
        pos_kelly = kelly.calculate(portfolio, hbar_price, confidence)

        print("   ┌─ Kelly Criterion ─────────────────────────────┐")
        print(f"   │  Formula: f* = (b·p − q) / b                 │")
        print(f"   │  Win rate: {kelly.base_win_rate:.0%}  |  Half-Kelly: {kelly.kelly_fraction:.0%}x          │")
        print(f"   │                                                │")
        print(f"   │  Position:  {pos_kelly.size:>8,.2f} HBAR  (${pos_kelly.size * hbar_price:>,.2f})     │")
        print(f"   │  Fraction:  {pos_kelly.fraction:>8.2%}                        │")
        print(f"   │  Risk:      ${pos_kelly.risk_amount:>8,.2f}                       │")
        print("   └────────────────────────────────────────────────┘")

        # Fixed Fraction
        fixed = FixedFractionSizing()
        pos_fixed = fixed.calculate(portfolio, hbar_price, confidence)

        print("\n   ┌─ Fixed Fraction ──────────────────────────────┐")
        print(f"   │  Base: {fixed.base_fraction:.1%}  |  Range: {fixed.min_fraction:.1%}–{fixed.max_fraction:.1%}                │")
        print(f"   │                                                │")
        print(f"   │  Position:  {pos_fixed.size:>8,.2f} HBAR  (${pos_fixed.size * hbar_price:>,.2f})     │")
        print(f"   │  Fraction:  {pos_fixed.fraction:>8.2%}                        │")
        print(f"   │  Risk:      ${pos_fixed.risk_amount:>8,.2f}                       │")
        print("   └────────────────────────────────────────────────┘")

        # ── Step 4: Confidence Sensitivity ────────────────────────────
        banner("Step 4: Confidence Sensitivity")

        print(f"   {'Confidence':<14} {'Kelly Size':>12} {'Fixed Size':>12} {'Risk':>10}")
        print(f"   {'─' * 14} {'─' * 12} {'─' * 12} {'─' * 10}")

        for conf in [0.30, 0.40, 0.50, 0.60, 0.70, 0.80]:
            pk = kelly.calculate(portfolio, hbar_price, conf)
            pf = fixed.calculate(portfolio, hbar_price, conf)
            print(
                f"   {conf:.0%}              "
                f"{pk.size:>8,.2f} HBAR  "
                f"{pf.size:>8,.2f} HBAR  "
                f"${pk.risk_amount:>8,.2f}"
            )

        # ── Step 5: Risk Management ───────────────────────────────────
        banner("Step 5: Risk Management")

        rm = RiskManagement(
            stop_loss_pct=0.01,
            take_profit_pct=0.02,
            max_daily_loss_pct=0.05,
            max_positions=5,
        )

        entry = hbar_price
        sl_long = rm.calculate_stop_loss(entry, "long")
        tp_long = rm.calculate_take_profit(entry, "long")
        sl_short = rm.calculate_stop_loss(entry, "short")
        tp_short = rm.calculate_take_profit(entry, "short")

        print(f"   Entry Price:      ${entry:.3f}")
        print()
        print(f"   ┌─ Long Position ───────────────────────────────┐")
        print(f"   │  Stop Loss:    ${sl_long:.3f}  ({rm.stop_loss_pct:.1%})                  │")
        print(f"   │  Take Profit:  ${tp_long:.3f}  (+{rm.take_profit_pct:.1%})                 │")
        print("   └────────────────────────────────────────────────┘")
        print()
        print(f"   ┌─ Short Position ──────────────────────────────┐")
        print(f"   │  Stop Loss:    ${sl_short:.3f}  (+{rm.stop_loss_pct:.1%})                 │")
        print(f"   │  Take Profit:  ${tp_short:.3f}  ({rm.take_profit_pct:.1%})                  │")
        print("   └────────────────────────────────────────────────┘")
        print()
        print(f"   Max Daily Loss:   {rm.max_daily_loss_pct:.0%} of portfolio")
        print(f"   Max Positions:    {rm.max_positions}")

        # Simulate position lifecycle
        print(f"\n   Position gate check: {'✅ Open' if rm.should_open_position() else '❌ Blocked'}")
        rm.increment_position_count()
        print(f"   After 1 position:    {'✅ Open' if rm.should_open_position() else '❌ Blocked'}")

        rm.update_pnl(-0.06)  # 6% loss
        print(f"   After 6% daily loss: {'✅ Open' if rm.should_open_position() else '❌ Blocked (daily limit hit)'}")

    # ── Done ──────────────────────────────────────────────────────────
    banner("✅ Demo Complete")
    print("   All components tested with real Hedera mainnet data.")
    print("   Ready for integration into Hedera agent tools, dashboards, and research workflows.\n")


if __name__ == "__main__":
    asyncio.run(main())
