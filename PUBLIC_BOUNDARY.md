# Public Boundary

This repository is the public Hedera tooling layer.

It is designed to be safe to read, run, fork, and build on without exposing private QVX/Veda infrastructure.

## Public In This Repository

- Hedera Mirror Node client code
- On-chain metric aggregation
- Position sizing and risk-management helpers
- Live public-data examples
- Documentation for Hedera agent use cases

## Kept Separate

QVX/Veda remains in-house technology. It may power future APIs, demos, and extracted tools, but the full internal stack is not part of this public repository.

Keep these out of this repo:

- Private keys and wallet files
- `.env` files and production credentials
- Exchange credentials
- Internal QVX/Veda runtime files
- Model checkpoints and generated training artifacts
- Logs, local databases, process IDs, and deployment state

## Future API Direction

Future public APIs should expose narrow, useful Hedera capabilities:

- Clean Mirror Node metric snapshots
- HCS-derived signal summaries
- Risk and sizing utilities
- Sanitized agent explanations

Those APIs should not expose private runtime internals, live operational strategy, or sensitive account data.
