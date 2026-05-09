# Getting Started

## Requirements

- Python 3.12+
- Internet access for Hedera Mirror Node public endpoints

## Option 1: One-Command Setup

From inside the repository:

```bash
bash setup.sh
source .venv/bin/activate
python3 demo.py
```

The setup script creates `.venv`, installs dependencies, and runs a syntax check.

## Option 2: Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Option 3: Editable Python Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

Use the public library API:

```python
from hedera_ml_pipeline import HederaMirrorNodeClient, HederaOnChainMetrics
```

See [docs/LIBRARY_API.md](docs/LIBRARY_API.md) for copy-paste examples.

## Option 4: Developer Install With Tests

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e ".[dev]"
pytest
```

## Run The Demo

```bash
python3 demo.py
```

## Run A JSON Snapshot

```bash
python3 examples/live_metrics_snapshot.py
```

## Run Agent Examples

```bash
python3 examples/network_health_agent.py
python3 examples/risk_gate_agent.py
```

## Validate The Repo

```bash
python3 -m py_compile demo.py examples/live_metrics_snapshot.py examples/network_health_agent.py examples/risk_gate_agent.py src/mirror_node.py src/metrics.py src/position_sizing.py src/risk_management.py
pytest
```

## Expected Result

The demo prints live Hedera network metrics, example position sizing, and risk-management output. The JSON snapshot example prints a structured object that can be reused by dashboards, notebooks, agents, or API prototypes. The agent examples print structured JSON reports for network health and risk-gate decisions.

## Next Steps

- Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Review [docs/FINDINGS.md](docs/FINDINGS.md)
- Review [VALIDATION.md](VALIDATION.md) and [LIMITATIONS.md](LIMITATIONS.md)
- Inspect `src/mirror_node.py`, `src/metrics.py`, `src/position_sizing.py`, and `src/risk_management.py`
