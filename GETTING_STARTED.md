# Getting Started

## Requirements

- Python 3.12+
- Internet access for Hedera Mirror Node public endpoints

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The Demo

```bash
python3 demo.py
```

## Run A JSON Snapshot

```bash
python3 examples/live_metrics_snapshot.py
```

## Expected Result

The demo prints live Hedera network metrics, example position sizing, and risk-management output. The JSON snapshot example prints a structured object that can be reused by dashboards, notebooks, agents, or API prototypes.

## Next Steps

- Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Review [docs/FINDINGS.md](docs/FINDINGS.md)
- Inspect `src/mirror_node.py`, `src/metrics.py`, `src/position_sizing.py`, and `src/risk_management.py`
