#!/usr/bin/env python3
"""
Network health agent example.

Fetches live Hedera mainnet metrics and turns them into an explainable health
summary that can be shown in a dashboard, sent to an operator, or passed to an
agent runtime.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.metrics import HederaOnChainMetrics
from src.mirror_node import HederaMirrorNodeClient


def build_health_report(metrics: Dict[str, Any]) -> Dict[str, Any]:
    staking = metrics.get("staking", {})
    supply = metrics.get("supply", {})
    transactions = metrics.get("transactions", {})

    score = 100
    watch_items: List[str] = []

    if staking.get("stake_total", 0) <= 0:
        score -= 35
        watch_items.append("staking metrics unavailable or zero")

    if supply.get("released_supply", 0) <= 0 or supply.get("total_supply", 0) <= 0:
        score -= 35
        watch_items.append("supply metrics unavailable or zero")

    if transactions.get("total_transactions", 0) <= 0:
        score -= 20
        watch_items.append("recent transaction sample is empty")

    if transactions.get("unique_accounts", 0) <= 1:
        score -= 10
        watch_items.append("recent transaction sample has low account diversity")

    score = max(0, min(100, score))
    status = "healthy" if score >= 80 else "watch" if score >= 50 else "degraded"

    return {
        "agent": "network_health_agent",
        "status": status,
        "score": score,
        "summary": (
            f"Hedera public metrics are {status}. "
            f"Sample includes {transactions.get('total_transactions', 0)} recent transactions "
            f"across {transactions.get('unique_accounts', 0)} observed accounts."
        ),
        "watch_items": watch_items,
        "metrics_used": {
            "stake_total_hbar": staking.get("stake_total"),
            "circulation_pct": supply.get("circulation_pct"),
            "recent_transactions": transactions.get("total_transactions"),
            "unique_accounts": transactions.get("unique_accounts"),
        },
    }


async def main() -> None:
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)
        snapshot = await metrics.get_all_metrics()

    report = build_health_report(snapshot)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(main())
