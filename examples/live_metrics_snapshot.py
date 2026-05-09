#!/usr/bin/env python3
"""
Live Hedera metrics snapshot.

This example is intentionally small: it fetches public Hedera mainnet Mirror Node
data and prints a JSON object that can be fed into dashboards, agents, notebooks,
or API prototypes.
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.metrics import HederaOnChainMetrics
from src.mirror_node import HederaMirrorNodeClient


async def main() -> None:
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)
        snapshot = await metrics.get_all_metrics()

    print(json.dumps(snapshot, indent=2, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(main())
