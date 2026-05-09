# Limitations

This project is intentionally scoped as public Hedera developer tooling. It is useful, but it is not a complete trading system or production agent runtime.

## Data Source Limits

- Mirror Node data is public and read-only.
- Public Mirror Node endpoints can be rate-limited or temporarily unavailable.
- Network latency depends on user location and endpoint conditions.
- Recent transaction samples are not full historical analytics unless pagination and storage are added.

## HCS Limits

- HCS topic messages are read from public Mirror Node topic endpoints.
- The raw `message` field is base64-encoded and must be decoded before parsing.
- Message schemas are not enforced yet.
- Chunked HCS messages are not reconstructed yet.
- Topic-specific trust, identity, and provenance rules must be designed by the application using this library.

## Agent Limits

- Example agents explain observations and risk gates; they do not autonomously execute transactions.
- No private keys, wallets, or account-signing flows are included.
- Risk gate examples are deterministic utilities, not financial advice.
- Agent memory, scheduling, retries, and production monitoring are outside the current scope.

## ML and Trading Limits

- Existing research found that basic technical indicators produced an honest baseline near chance after data leakage fixes.
- The repository does not claim predictive trading performance.
- Position sizing and risk-management helpers reduce operational risk, but they do not guarantee profitability.
- Backtesting examples are planned but not included yet.

## Public Boundary

QVX/Veda runtime internals, secrets, generated model artifacts, databases, logs, and deployment state are intentionally excluded. See [PUBLIC_BOUNDARY.md](PUBLIC_BOUNDARY.md).
