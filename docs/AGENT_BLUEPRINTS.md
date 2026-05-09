# Hedera Agent Blueprints

Practical agent patterns that can be built on top of public Hedera Mirror Node data and the tooling in this repository.

These blueprints are intentionally narrow: they use public data, avoid private keys, and keep execution decisions separate from observation and analysis.

## 1. Network Health Agent

**Goal:** Explain current Hedera network state in a compact, operator-friendly format.

**Inputs:**
- Network stake
- Released supply
- Recent transaction volume
- Unique active accounts in recent transactions

**Outputs:**
- Health score
- Human-readable summary
- Watch items for dashboards or alerts

**Example decisions:**
- Healthy: transaction sample available, staking data available, supply data available
- Degraded: one or more public endpoints unavailable
- Watch: unusually low transaction sample or missing account activity

**Starter:** `examples/network_health_agent.py`

## 2. Risk Gate Agent

**Goal:** Decide whether a downstream model, rule engine, or human operator is allowed to open a position.

**Inputs:**
- Signal confidence
- Portfolio value
- Current HBAR price
- Current open position count
- Daily P&L state

**Outputs:**
- Allow/block decision
- Suggested position size
- Stop-loss and take-profit levels
- Explanation of the risk gate

**Example decisions:**
- Allow a small position if daily loss and position limits are clear
- Block a trade if daily loss limit is breached
- Block a trade if maximum open positions are reached

**Starter:** `examples/risk_gate_agent.py`

## 3. HCS Signal Watcher Agent

**Goal:** Read HCS topic messages and convert them into structured context for an agent system.

**Inputs:**
- Topic IDs (list of strings, e.g., `["0.0.12345"]`)

**Outputs:**
```python
{
    "agent": "hcs_signal_watcher",
    "topics": ["0.0.12345"],
    "signal_count": 1,
    "signals": [
        {
            "topic_id": "0.0.12345",
            "sequence_number": 1,
            "content": {"signal": "watch", "score": 0.75},
            "raw_message": "...",
            "timestamp": "1714953600.123456789"
        }
    ],
    "timestamp": "2026-05-09T..."
}
```

**Status:** The base Mirror Node topic method exists and decodes base64 messages before parsing JSON/text content. Schema validation, chunk reconstruction, and topic-specific trust rules are planned.

**Starter:** `examples/hcs_signal_watcher.py`

## 4. Treasury Monitor Agent

**Goal:** Watch selected Hedera accounts or token balances and summarize treasury state.

**Inputs:**
- Account ID (string, e.g., `"0.0.12345"`)

**Outputs:**
```python
{
    "agent": "treasury_monitor",
    "account_id": "0.0.12345",
    "balance": 12345.67,
    "key_expiry": 1714953600,
    "auto_renew_period": 7776000,
    "recent_tx_count": 5,
    "timestamp": "2026-05-09T..."
}
```

**Status:** Account and token endpoints exist in `src/mirror_node.py`. A dedicated example can be added next.

**Starter:** `examples/treasury_monitor.py`

## 5. Public Metrics API Agent

**Goal:** Serve a minimal public JSON endpoint for Hedera metrics without exposing internal infrastructure.

**Inputs:**
- Network (string, default `"mainnet"`)

**Outputs:**
```python
{
    "staking": {...},
    "supply": {...},
    "transactions": {...}
}
```

**Status:** `get_live_metrics()` convenience helper exists in the public API.

**Starter:** `examples/dashboard_export.py`

## 6. Research Agent

**Goal:** Combine Hedera on-chain metrics with market data, notebooks, or models to test hypotheses.

**Inputs:**
- Staking metrics
- Supply metrics
- Transaction volume
- External market data

**Outputs:**
- Feature snapshots
- Backtest-ready rows
- Research notes and reproducible experiments

**Status:** Current repo provides live metrics and risk helpers. Backtesting examples are on the roadmap.

## Design Rules

- Agents should explain decisions, not only output numbers.
- Public examples should not require private keys.
- Risk gates should be separate from signal generation.
- Mirror Node data should be cached or rate-limited for production use.
- QVX/Veda runtime internals stay outside this public repository.

## Validation

Runnable examples are documented in [../VALIDATION.md](../VALIDATION.md). Current public examples cover live metrics snapshots, a network health agent, and a risk gate agent.

## Limitations

Known limitations are documented in [../LIMITATIONS.md](../LIMITATIONS.md), including HCS schema validation, chunked messages, production monitoring, and the boundary between this public repo and in-house QVX/Veda systems.
