#!/usr/bin/env python3
"""
Example integration with pandas for data analysis.

Shows how to convert Hedera metrics into pandas DataFrames for analysis.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from hedera_ml_pipeline import get_live_metrics


async def main():
    metrics = await get_live_metrics()

    # Convert metrics to DataFrames
    staking_df = pd.DataFrame([metrics["staking"]])
    supply_df = pd.DataFrame([metrics["supply"]])
    tx_df = pd.DataFrame([metrics["transactions"]])

    print("=== Staking Metrics ===")
    print(staking_df.to_string(index=False))

    print("\n=== Supply Metrics ===")
    print(supply_df.to_string(index=False))

    print("\n=== Transaction Metrics ===")
    print(tx_df.to_string(index=False))

    # Example: combine into summary
    summary = pd.DataFrame({
        "metric": ["stake_total", "circulating_supply", "recent_tx_count"],
        "value": [
            metrics["staking"]["stake_total"],
            metrics["supply"]["released_supply"],
            metrics["transactions"]["total_transactions"],
        ]
    })
    print("\n=== Summary ===")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    asyncio.run(main())
