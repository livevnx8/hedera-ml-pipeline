#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hedera_ml_pipeline import HederaMirrorNodeClient


async def main(account_id: str):
    async with HederaMirrorNodeClient("mainnet") as client:
        account = await client.get_account(account_id)
        transactions = await client.get_transactions(account_id=account_id, limit=10)

        print({
            "agent": "treasury_monitor",
            "account_id": account_id,
            "balance": float(account.get("balance", {}).get("balance", 0)) / 1e8,
            "key_expiry": account.get("key_expiry"),
            "auto_renew_period": account.get("auto_renew_period"),
            "recent_tx_count": len(transactions),
            "timestamp": account.get("timestamp"),
        })


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Monitor a Hedera treasury account from mainnet.")
    parser.add_argument("account_id", help="Hedera account ID (e.g., 0.0.12345)")
    args = parser.parse_args()

    asyncio.run(main(args.account_id))
