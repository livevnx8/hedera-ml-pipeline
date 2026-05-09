# Use Cases

## On-Chain Intelligence Agents

Agents can query Hedera Mirror Node data, convert it into structured metrics, and feed those metrics into downstream models, rule engines, or dashboards.

Examples:

- Network health agents that summarize live staking, supply, and transaction activity.
- Treasury monitor agents that watch selected accounts and token balances.
- Research agents that collect feature snapshots for notebooks and backtests.

## Risk-Aware Execution Agents

The pipeline includes position sizing and risk gates so an agent can separate signal confidence from execution permission.

Examples:

- Risk gate agents that approve, resize, or block proposed actions.
- Policy agents that enforce daily loss limits and open-position caps.
- Explanation agents that produce an audit-friendly reason for each decision.

## HCS Signal Pipelines

Hedera Consensus Service topics can act as durable coordination streams for signals, provenance, and shared agent context.

Examples:

- HCS signal watcher agents that monitor topic messages.
- Provenance agents that attach topic ID, sequence number, and consensus timestamp to each signal.
- Coordination agents that use HCS as a shared message rail between services.

## Operator Dashboards

The metrics layer can feed dashboards that explain network state, staking, transaction activity, and agent decisions.

Examples:

- Live network health panels.
- Risk state panels showing daily P&L, open positions, and active limits.
- Agent decision timelines backed by public Hedera data.

## API Prototypes

The live snapshot example can become the first shape of a public API: a narrow endpoint that exposes useful Hedera metrics without exposing internal QVX/Veda runtime details.

## Research and Backtesting

Developers can combine Hedera on-chain metrics with market data to test strategies, agent policies, and execution rules.
