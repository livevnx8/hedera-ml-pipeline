#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hedera_ml_pipeline import HederaMirrorNodeClient, HederaOnChainMetrics


async def main(topic_ids: list[str]):
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)
        result = await metrics.get_hcs_signals(topic_ids)

        print({
            "agent": "hcs_signal_watcher",
            "topics": topic_ids,
            "signal_count": result["signal_count"],
            "signals": result["signals"],
            "timestamp": result["timestamp"],
        })


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Watch HCS topic signals from Hedera mainnet.")
    parser.add_argument("topic_ids", nargs="+", help="HCS topic IDs (e.g., 0.0.12345)")
    args = parser.parse_args()

    asyncio.run(main(args.topic_ids))
