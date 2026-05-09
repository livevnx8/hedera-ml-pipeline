# Contributing

Contributions are welcome when they improve Hedera data access, agent infrastructure, tests, documentation, or reproducibility.

## Local Checks

```bash
python3 -m py_compile demo.py examples/live_metrics_snapshot.py examples/network_health_agent.py examples/risk_gate_agent.py src/mirror_node.py src/metrics.py src/position_sizing.py src/risk_management.py
python3 examples/risk_gate_agent.py
```

For live Mirror Node validation, also run:

```bash
python3 demo.py
python3 examples/live_metrics_snapshot.py
python3 examples/network_health_agent.py
```

## Pull Requests

- Keep changes focused.
- Document new public behavior.
- Avoid committing generated data, local logs, private credentials, or model artifacts.
- Explain how you verified the change.
