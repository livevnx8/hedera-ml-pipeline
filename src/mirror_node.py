"""
Hedera Mirror Node API client.
Provides async access to Hedera network data with no authentication required.
"""

import aiohttp
from typing import Dict, Any, Optional, List


class HederaMirrorNodeClient:
    """
    Client for Hedera Mirror Node REST API.

    The Mirror Node provides read-only access to Hedera network data including
    transactions, accounts, tokens, topics, and network metrics. No API key required.

    Base URLs:
        Mainnet:  https://mainnet-public.mirrornode.hedera.com/api/v1
        Testnet:  https://testnet.mirrornode.hedera.com/api/v1
        Previewnet: https://previewnet.mirrornode.hedera.com/api/v1

    Rate Limit: 50 requests/second per IP on mainnet.
    """

    NETWORKS = {
        "mainnet": "https://mainnet-public.mirrornode.hedera.com/api/v1",
        "testnet": "https://testnet.mirrornode.hedera.com/api/v1",
        "previewnet": "https://previewnet.mirrornode.hedera.com/api/v1",
    }

    def __init__(self, network: str = "mainnet"):
        """
        Initialize the Mirror Node client.

        Args:
            network: One of 'mainnet', 'testnet', or 'previewnet'.
        """
        if network not in self.NETWORKS:
            raise ValueError(f"Unknown network '{network}'. Use: {list(self.NETWORKS.keys())}")
        self.network = network
        self.base_url = self.NETWORKS[network]
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a GET request to the Mirror Node API."""
        if not self.session:
            raise RuntimeError("Use 'async with HederaMirrorNodeClient() as client:' context manager.")

        url = f"{self.base_url}{endpoint}"
        async with self.session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()

    # ── Network Endpoints ──────────────────────────────────────────────

    async def get_network_stake(self) -> Dict[str, Any]:
        """
        Get network staking information.

        Returns:
            Dict with: max_staking_reward_rate_per_hbar, node_reward_fee_fraction,
            stake_total, staking_period, staking_reward_rate, staking_start_threshold.
        """
        return await self._get("/network/stake")

    async def get_network_supply(self) -> Dict[str, Any]:
        """
        Get HBAR token supply.

        Returns:
            Dict with: released_supply (circulating), total_supply (50B cap), timestamp.
        """
        return await self._get("/network/supply")

    async def get_network_fees(self) -> Dict[str, Any]:
        """
        Get network fee schedule.

        Returns:
            Dict with fee information for each transaction type.
        """
        return await self._get("/network/fees")

    async def get_network_exchange_rate(self) -> Dict[str, Any]:
        """
        Get HBAR-to-tinybar exchange rate.

        Returns:
            Dict with current, next, and expiration exchange rates.
        """
        return await self._get("/network/exchangerate")

    # ── Transaction Endpoints ──────────────────────────────────────────

    async def get_transactions(
        self,
        account_id: Optional[str] = None,
        transaction_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get recent transactions.

        Args:
            account_id: Filter by account ID (e.g., '0.0.12345').
            transaction_type: Filter by type (e.g., 'CRYPTOTRANSFER', 'CONTRACTCALL').
            limit: Max results (default 100).

        Returns:
            List of transaction objects with transfers, fees, and timestamps.
        """
        params = {"limit": limit}
        if account_id:
            params["account.id"] = account_id
        if transaction_type:
            params["transactiontype"] = transaction_type

        result = await self._get("/transactions", params)
        return result.get("transactions", [])

    async def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get a specific transaction by ID.

        Args:
            transaction_id: Transaction ID (e.g., '0.0.12345@1234567890.000000000').

        Returns:
            Full transaction details including transfers, fees, and result.
        """
        return await self._get(f"/transactions/{transaction_id}")

    # ── Account Endpoints ──────────────────────────────────────────────

    async def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get account information.

        Args:
            account_id: Account ID (e.g., '0.0.12345').

        Returns:
            Account details: balance, key, expiry, auto-renew, etc.
        """
        return await self._get(f"/accounts/{account_id}")

    # ── Token Endpoints ────────────────────────────────────────────────

    async def get_token(self, token_id: str) -> Dict[str, Any]:
        """
        Get token information.

        Args:
            token_id: Token ID (e.g., '0.0.12345').

        Returns:
            Token details: name, symbol, decimals, total supply, etc.
        """
        return await self._get(f"/tokens/{token_id}")

    async def get_token_balances(
        self, token_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get token balance distribution.

        Args:
            token_id: Token ID.
            limit: Max results.

        Returns:
            List of account balances for the token.
        """
        params = {"limit": limit}
        result = await self._get(f"/tokens/{token_id}/balances", params)
        return result.get("balances", [])

    # ── Topic (HCS) Endpoints ──────────────────────────────────────────

    async def get_topic_messages(
        self, topic_id: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get messages from an HCS topic.

        Args:
            topic_id: HCS topic ID.
            limit: Max messages.

        Returns:
            List of messages with sequence_number, message (base64), consensus_timestamp.
        """
        params = {"limit": limit}
        result = await self._get(f"/topics/{topic_id}/messages", params)
        return result.get("messages", [])
