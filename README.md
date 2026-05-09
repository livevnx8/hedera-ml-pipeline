# Hedera ML Pipeline

Hedera-native data and risk infrastructure for AI agents.

This project turns public Hedera Mirror Node data into structured metrics that agent systems can use for research, monitoring, signal generation, dashboards, and risk-aware automation.

## Product Snapshot

| Area | Included |
| --- | --- |
| Data access | Async Hedera Mirror Node client |
| Metrics | Staking, supply, transaction activity, HCS-ready signal parsing |
| Agents | Network health and risk gate examples |
| Risk | Kelly sizing, fixed-fraction sizing, stop-loss, take-profit, daily limits |
| Validation | Live examples, syntax checks, documented limitations |
| Boundary | Public tooling only; private runtime state and QVX/Veda internals excluded |

## What It Does

- Reads public Hedera Mirror Node endpoints with an async Python client.
- Aggregates staking, supply, transaction, and HCS-oriented metrics.
- Provides position sizing helpers using Kelly and fixed-fraction approaches.
- Provides risk-management helpers for stops, take-profit levels, daily limits, and position caps.
- Documents benchmark results and lessons from ML leakage testing.

## Why Hedera

Hedera gives builders low-latency public network data, native staking data, HCS message streams, and high-throughput infrastructure that can become useful context for agents.

This pipeline starts with Hedera-specific primitives instead of generic exchange-only data, making it a clean foundation for Hedera tools and future agent APIs.

## Agent Use Cases

- On-chain intelligence agents that monitor network state.
- HCS signal pipelines that coordinate shared context.
- Network health agents that summarize staking, supply, and recent transaction activity.
- Risk gate agents that approve or block proposed actions before execution.
- Operator dashboards that explain network and execution state.
- Risk-aware execution systems that separate signal confidence from action permission.
- Research pipelines that combine Hedera metrics with model, rule, or LLM reasoning.

See [USE_CASES.md](USE_CASES.md) and [docs/AGENT_BLUEPRINTS.md](docs/AGENT_BLUEPRINTS.md) for a fuller map.

## Architecture

```text
Hedera Mirror Node
        |
        v
HederaMirrorNodeClient
        |
        v
HederaOnChainMetrics
        |
        +--> Staking metrics
        +--> Supply metrics
        +--> Transaction metrics
        +--> HCS-oriented signals
        |
        v
Agent / model / rule engine
        |
        v
Position sizing + risk gates
```

More detail is available in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Quick Start

Fastest setup:

```bash
git clone https://github.com/livevnx8/hedera-ml-pipeline.git
cd hedera-ml-pipeline
bash setup.sh
source .venv/bin/activate
python3 demo.py
```

Manual setup:

```bash
git clone https://github.com/livevnx8/hedera-ml-pipeline.git
cd hedera-ml-pipeline
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 demo.py
```

The demo reads live public Hedera data and prints network metrics, example sizing output, and risk-management output.

## Live Data Example

For a compact JSON snapshot from real Hedera mainnet data:

```bash
python3 examples/live_metrics_snapshot.py
```

That output is meant to be easy to feed into dashboards, agent prompts, notebooks, or API prototypes.

For runnable agent-style examples:

```bash
python3 examples/network_health_agent.py
python3 examples/risk_gate_agent.py
```

See [examples/README.md](examples/README.md) for the full examples index.

## Documentation

- [Getting Started](GETTING_STARTED.md)
- [Use Cases](USE_CASES.md)
- [Advantages](ADVANTAGES.md)
- [Validation](VALIDATION.md)
- [Limitations](LIMITATIONS.md)
- [Agent Blueprints](docs/AGENT_BLUEPRINTS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API_REFERENCE.md)
- [Benchmarks](docs/BENCHMARKS.md)
- [Research Findings](docs/FINDINGS.md)
- [Public Boundary](PUBLIC_BOUNDARY.md)
- [Roadmap](ROADMAP.md)
- [Security](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## Benchmarks

Measured against Hedera mainnet public Mirror Node endpoints:

| Metric | Value | Notes |
| --- | ---: | --- |
| Mirror Node latency, single call | ~25 ms | `/network/stake` |
| Full metrics fetch, 3 parallel calls | ~30 ms | Stake, supply, transactions |
| Kelly calculation | <0.1 ms | Pure math |
| Position sizing plus risk check | <0.2 ms | Combined local pipeline |
| ONNX quantized inference reference | 14 us | From broader QVX optimization work |

See [docs/BENCHMARKS.md](docs/BENCHMARKS.md) for details and test conditions.

## Safety and Scope

This is research and developer tooling. It is not financial advice and does not guarantee trading performance.

The included demo does not require private keys. Do not connect production funds, private endpoints, wallet files, or exchange credentials without independent review and appropriate controls.

Known limitations are documented in [LIMITATIONS.md](LIMITATIONS.md). Validation commands are documented in [VALIDATION.md](VALIDATION.md).

QVX/Veda remains in-house technology. This repository is the public Hedera tooling layer and should stay clean of internal runtime files, secrets, generated model artifacts, logs, and deployment state. See [PUBLIC_BOUNDARY.md](PUBLIC_BOUNDARY.md).

## Roadmap

- Hedera Mirror Node async client: complete
- On-chain metrics aggregation: complete
- Position sizing and risk helpers: complete
- Network health and risk gate agent examples: complete
- HCS signal parsing with schema validation: next
- Backtesting and dashboard examples: next
- Selected integrations with in-house QVX/Veda-backed tools and APIs: later

## License

MIT. See [LICENSE](LICENSE).
