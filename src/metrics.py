"""
On-chain metrics aggregation for Hedera trading signals.
Processes raw Mirror Node data into actionable trading metrics.
"""

import asyncio
import base64
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from .mirror_node import HederaMirrorNodeClient
from .hcs_schemas import validate_hcs_signal


class HederaOnChainMetrics:
    """
    Aggregates Hedera on-chain data into trading signal metrics.

    Provides:
    - Staking metrics (total stake, reward rate)
    - Supply metrics (circulation %, release rate)
    - Transaction volume (count, unique accounts, avg value)
    - HCS topic signals (parsed messages)
    """

    def __init__(self, client: HederaMirrorNodeClient):
        self.client = client

    async def get_staking_metrics(self) -> Dict[str, Any]:
        """
        Fetch and process staking metrics.

        Returns:
            Dict with:
            - stake_total: Total HBAR staked (in HBAR)
            - staking_reward_rate: Current reward rate
            - max_reward_rate: Maximum reward rate per HBAR
        """
        data = await self.client.get_network_stake()

        return {
            "stake_total": float(data.get("stake_total", 0)) / 1e8,
            "staking_reward_rate": float(data.get("staking_reward_rate", 0)),
            "max_reward_rate": float(data.get("max_staking_reward_rate_per_hbar", 0)),
            "timestamp": datetime.now().isoformat(),
        }

    async def get_supply_metrics(self) -> Dict[str, Any]:
        """
        Fetch and process supply metrics.

        Returns:
            Dict with:
            - released_supply: HBAR in circulation
            - total_supply: Maximum HBAR supply (50B)
            - circulation_pct: Percentage of total supply circulating
        """
        data = await self.client.get_network_supply()

        released = float(data.get("released_supply", 0)) / 1e8
        total = float(data.get("total_supply", 0)) / 1e8

        return {
            "released_supply": released,
            "total_supply": total,
            "circulation_pct": round((released / total) * 100, 2) if total > 0 else 0,
            "timestamp": datetime.now().isoformat(),
        }

    async def get_transaction_volume(self) -> Dict[str, Any]:
        """
        Fetch and process transaction volume metrics.

        Returns:
            Dict with:
            - total_transactions: Number of transactions in sample
            - unique_accounts: Distinct accounts involved
            - avg_transaction_value: Average HBAR transferred per tx
        """
        transactions = await self.client.get_transactions(limit=100)

        accounts = set()
        total_value = 0.0

        for tx in transactions:
            transfers = tx.get("transfers", [])
            for transfer in transfers:
                accounts.add(transfer.get("account"))
                total_value += abs(float(transfer.get("amount", 0))) / 1e8

        return {
            "total_transactions": len(transactions),
            "unique_accounts": len(accounts),
            "avg_transaction_value": round(total_value / len(transactions), 4) if transactions else 0,
            "timestamp": datetime.now().isoformat(),
        }

    async def get_hcs_signals(
        self, topic_ids: List[str], validate_schemas: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch and parse HCS topic messages.

        Args:
            topic_ids: List of HCS topic IDs to query.
            validate_schemas: If True, validate parsed content against known schemas.

        Returns:
            Dict with:
            - signals: Parsed messages with optional validation results
            - signal_count: Number of signals found
        """
        all_messages = []

        for topic_id in topic_ids:
            try:
                messages = await self.client.get_topic_messages(topic_id, limit=10)
                all_messages.extend(messages)
            except Exception as e:
                print(f"  [warn] Could not fetch topic {topic_id}: {e}")

        signals = []
        for msg in all_messages:
            raw = msg.get("message", "")
            decoded = raw
            if isinstance(raw, str):
                try:
                    decoded = base64.b64decode(raw).decode("utf-8")
                except Exception:
                    decoded = raw

            try:
                content = json.loads(decoded)
            except (json.JSONDecodeError, TypeError):
                content = decoded

            signal = {
                "topic_id": msg.get("topic_id"),
                "sequence_number": msg.get("sequence_number"),
                "content": content,
                "raw_message": raw,
                "timestamp": msg.get("consensus_timestamp"),
            }

            if validate_schemas and isinstance(content, dict):
                validation = validate_hcs_signal(content)
                signal["validation"] = validation

            signals.append(signal)

        return {
            "signals": signals,
            "signal_count": len(signals),
            "timestamp": datetime.now().isoformat(),
        }

    async def get_all_metrics(
        self, hcs_topic_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Fetch all on-chain metrics in parallel.

        Args:
            hcs_topic_ids: Optional HCS topic IDs to include.

        Returns:
            Full metrics dict with staking, supply, transactions, and optional HCS.
        """
        tasks = [
            self.get_staking_metrics(),
            self.get_supply_metrics(),
            self.get_transaction_volume(),
        ]

        if hcs_topic_ids:
            tasks.append(self.get_hcs_signals(hcs_topic_ids))

        results = await asyncio.gather(*tasks)

        metrics = {
            "staking": results[0],
            "supply": results[1],
            "transactions": results[2],
        }

        if hcs_topic_ids:
            metrics["hcs"] = results[3]

        return metrics
