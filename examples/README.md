# Examples

Runnable examples for Hedera-native agent workflows.

All examples use public Hedera Mirror Node endpoints and require no private keys.

## Live Metrics Snapshot

```bash
python3 examples/live_metrics_snapshot.py
```

Prints a compact JSON object with staking, supply, and transaction metrics.

## Network Health Agent

```bash
python3 examples/network_health_agent.py
```

Fetches live Hedera mainnet metrics and returns an explainable health report with:

- Status
- Score
- Summary
- Watch items
- Metrics used

## Risk Gate Agent

```bash
python3 examples/risk_gate_agent.py
```

Turns a signal confidence value into a proposed HBAR position and runs it through risk controls.

The output includes:

- Allow/block decision
- Reason
- Position size
- Portfolio fraction
- Stop-loss and take-profit levels

## HCS Signal Watcher

```bash
python3 examples/hcs_signal_watcher.py 0.0.12345
```

Fetches and decodes HCS topic messages from Hedera mainnet.

Output includes:

- Topic IDs
- Signal count
- Decoded signals with content
- Timestamp

## Treasury Monitor

```bash
python3 examples/treasury_monitor.py 0.0.12345
```

Monitors a Hedera account balance and recent transaction activity from mainnet.

Output includes:

- Account ID
- Balance in HBAR
- Key expiry
- Auto-renew period
- Recent transaction count

## Dashboard Export

```bash
python3 examples/dashboard_export.py
```

Emits a stable JSON metrics snapshot suitable for dashboards, APIs, or notebooks.

## Notes

- These examples are developer tooling, not financial advice.
- Public Mirror Node endpoints can be rate-limited or temporarily unavailable.
- The examples are intentionally narrow so they can be reused in dashboards, notebooks, APIs, or agent runtimes.
