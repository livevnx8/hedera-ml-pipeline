# API Reference

Complete reference for the Hedera Mirror Node REST API endpoints supported by this pipeline.

## Base URLs

| Network | URL |
|---------|-----|
| Mainnet | `https://mainnet-public.mirrornode.hedera.com/api/v1` |
| Testnet | `https://testnet.mirrornode.hedera.com/api/v1` |
| Previewnet | `https://previewnet.mirrornode.hedera.com/api/v1` |

**Rate Limit:** 50 requests/second per IP on mainnet.
**Authentication:** None required.

---

## Network Endpoints

### `GET /network/stake`

Returns network staking information.

**Response:**
```json
{
  "max_staking_reward_rate_per_hbar": 5912,
  "node_reward_fee_fraction": 0.0,
  "stake_total": "1630630638200000000",
  "staking_period": {
    "from": "1714867200.000000000",
    "to": "1714953600.000000000"
  },
  "staking_period_duration": 1440,
  "staking_periods_stored": 365,
  "staking_reward_fee_fraction": 0.0,
  "staking_reward_rate": 44517770647520,
  "staking_start_threshold": 25000000000000000
}
```

**Python:**
```python
data = await client.get_network_stake()
staked = float(data["stake_total"]) / 1e8  # Convert tinybars → HBAR
```

### `GET /network/supply`

Returns HBAR token supply information.

**Response:**
```json
{
  "released_supply": "4337314165520758000",
  "timestamp": "1714953600.971360000",
  "total_supply": "5000000000000000000"
}
```

**Python:**
```python
data = await client.get_network_supply()
circulation_pct = (float(data["released_supply"]) / float(data["total_supply"])) * 100
```

### `GET /network/fees`

Returns the network fee schedule for all transaction types.

**Response:**
```json
{
  "fees": [
    {
      "gas": 0,
      "transaction_type": "CRYPTOTRANSFER"
    }
  ],
  "timestamp": "1714953600.123456789"
}
```

### `GET /network/exchangerate`

Returns the HBAR-to-tinybar and HBAR-to-USD exchange rates.

**Response:**
```json
{
  "current_rate": {
    "cent_equivalent": 596987,
    "expiration_time": 1714953600,
    "hbar_equivalent": 30000
  },
  "next_rate": {
    "cent_equivalent": 600000,
    "expiration_time": 1715040000,
    "hbar_equivalent": 30000
  }
}
```

---

## Transaction Endpoints

### `GET /transactions`

Returns a paginated list of transactions.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `account.id` | string | Filter by account ID |
| `transactiontype` | string | Filter by type (CRYPTOTRANSFER, CONTRACTCALL, etc.) |
| `limit` | integer | Max results (default 25, max 100) |
| `order` | string | Sort order: `asc` or `desc` |
| `timestamp` | string | Filter by consensus timestamp |

**Response:**
```json
{
  "transactions": [
    {
      "bytes": null,
      "charged_tx_fee": 568000,
      "consensus_timestamp": "1714953600.123456789",
      "entity_id": null,
      "max_fee": "1000000",
      "memo_base64": "",
      "name": "CRYPTOTRANSFER",
      "node": "0.0.3",
      "nonce": 0,
      "parent_consensus_timestamp": null,
      "result": "SUCCESS",
      "scheduled": false,
      "transaction_hash": "abc123...",
      "transaction_id": "0.0.12345@1714953600.123456789",
      "transfers": [
        {
          "account": "0.0.12345",
          "amount": 100000000,
          "is_approval": false
        }
      ]
    }
  ],
  "links": {
    "next": "/api/v1/transactions?limit=100&timestamp=lt:1714953600.123456789"
  }
}
```

### `GET /transactions/{transactionId}`

Returns a single transaction by ID.

**Path Parameter:** `transactionId` — Format: `0.0.12345@1234567890.000000000`

---

## Account Endpoints

### `GET /accounts/{accountId}`

Returns account information.

**Response:**
```json
{
  "account": "0.0.12345",
  "alias": null,
  "auto_renew_period": 7776000,
  "balance": {
    "balance": 1000000000,
    "timestamp": "1714953600.123456789"
  },
  "created_timestamp": "1600000000.000000000",
  "decline_reward": false,
  "deleted": false,
  "ethereum_nonce": 0,
  "evm_address": null,
  "expiry_timestamp": "1800000000.000000000",
  "key": {
    "_type": "ED25519",
    "key": "abc123..."
  },
  "max_automatic_token_associations": 0,
  "memo": "",
  "pending_reward": 0,
  "receiver_sig_required": false,
  "staked_account_id": null,
  "staked_node_id": 0,
  "stake_period_start": null
}
```

---

## Token Endpoints

### `GET /tokens/{tokenId}`

Returns token information.

### `GET /tokens/{tokenId}/balances`

Returns token balance distribution.

**Query Parameters:** `limit` (max 100), `order`, `account.id`

---

## Topic (HCS) Endpoints

### `GET /topics/{topicId}/messages`

Returns messages from an HCS topic.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Max results (default 25, max 100) |
| `order` | string | Sort order: `asc` or `desc` |
| `sequencenumber` | integer | Filter by sequence number |

**Response:**
```json
{
  "messages": [
    {
      "chunk_info": null,
      "consensus_timestamp": "1714953600.123456789",
      "message": "SGVsbG8gV29ybGQ=",
      "payer_account_id": "0.0.12345",
      "running_hash": "abc123...",
      "running_hash_version": 3,
      "sequence_number": 1,
      "topic_id": "0.0.12345"
    }
  ],
  "links": {
    "next": null
  }
}
```

**Note:** The `message` field is base64-encoded. Decode before JSON parsing or text processing:
```python
import base64
decoded = base64.b64decode(msg["message"]).decode("utf-8")
```

`HederaOnChainMetrics.get_hcs_signals()` performs this decode step and returns both `content` and `raw_message`.

---

## Error Responses

All endpoints return standard HTTP error codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Invalid parameter |
| 404 | Entity not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

---

## Python Client Reference

### `HederaMirrorNodeClient`

```python
class HederaMirrorNodeClient(network: str = "mainnet")
```

**Methods:**
- `get_network_stake() → Dict`
- `get_network_supply() → Dict`
- `get_network_fees() → Dict`
- `get_network_exchange_rate() → Dict`
- `get_transactions(account_id, transaction_type, limit) → List[Dict]`
- `get_transaction(transaction_id) → Dict`
- `get_account(account_id) → Dict`
- `get_token(token_id) → Dict`
- `get_token_balances(token_id, limit) → List[Dict]`
- `get_topic_messages(topic_id, limit) → List[Dict]`

### `HederaOnChainMetrics`

```python
class HederaOnChainMetrics(client: HederaMirrorNodeClient)
```

**Methods:**
- `get_staking_metrics() → Dict`
- `get_supply_metrics() → Dict`
- `get_transaction_volume() → Dict`
- `get_hcs_signals(topic_ids) → Dict`
- `get_all_metrics(hcs_topic_ids) → Dict`
