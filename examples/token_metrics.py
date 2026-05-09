#!/usr/bin/env python3
"""
Example for fetching token supply and distribution metrics from Hedera.

This demonstrates how to use the Mirror Node client to get token information.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hedera_ml_pipeline import HederaMirrorNodeClient


async def main(token_id: str):
    async with HederaMirrorNodeClient("mainnet") as client:
        token = await client.get_token(token_id)

        print({
            "agent": "token_metrics",
            "token_id": token_id,
            "name": token.get("name"),
            "symbol": token.get("symbol"),
            "total_supply": float(token.get("total_supply", 0)) / 1e8,
            "decimals": token.get("decimals"),
            "timestamp": token.get("timestamp"),
        })


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fetch token metrics from Hedera mainnet.")
    parser.add_argument("token_id", help="Hedera token ID (e.g., 0.0.12345)")
    args = parser.parse_args()

    asyncio.run(main(args.token_id))
