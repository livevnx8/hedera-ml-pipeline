#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found."
  exit 1
fi

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

python3 -m py_compile \
  demo.py \
  examples/live_metrics_snapshot.py \
  examples/network_health_agent.py \
  examples/risk_gate_agent.py \
  src/mirror_node.py \
  src/metrics.py \
  src/position_sizing.py \
  src/risk_management.py

echo "Setup complete."
echo "Run: source .venv/bin/activate"
echo "Then: python3 demo.py"
