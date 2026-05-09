# Validation

This repository includes lightweight validation commands that can be run before publishing or after cloning.

## Environment Check

```bash
python3 --version
python3 -m pip install -r requirements.txt
```

## Setup Check

```bash
bash setup.sh
source .venv/bin/activate
```

## Live Examples

These commands use public Hedera mainnet Mirror Node endpoints. No private keys or API keys are required.

```bash
python3 demo.py
python3 examples/live_metrics_snapshot.py
python3 examples/network_health_agent.py
python3 examples/risk_gate_agent.py
```

Expected result:

- `demo.py` prints live staking, supply, transaction, sizing, and risk-management output.
- `examples/live_metrics_snapshot.py` prints a JSON metrics object.
- `examples/network_health_agent.py` prints an explainable health report.
- `examples/risk_gate_agent.py` prints an allow/block risk gate decision.

## Syntax Check

```bash
python3 -m py_compile \
  demo.py \
  examples/live_metrics_snapshot.py \
  examples/network_health_agent.py \
  examples/risk_gate_agent.py \
  src/mirror_node.py \
  src/metrics.py \
  src/position_sizing.py \
  src/risk_management.py
```

## Git Verification

```bash
git status --short --branch
git remote -v
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

The local commit and remote `refs/heads/main` should match after a successful push.
