# Contributing

Contributions are welcome when they improve Hedera data access, agent infrastructure, tests, documentation, or reproducibility.

## Local Checks

```bash
python3 -m pip install -e ".[dev]"
pytest
python3 -m py_compile demo.py examples/live_metrics_snapshot.py examples/network_health_agent.py examples/risk_gate_agent.py src/mirror_node.py src/metrics.py src/position_sizing.py src/risk_management.py hedera_ml_pipeline/__init__.py hedera_ml_pipeline/api.py
```

For live Mirror Node validation, also run:

```bash
python3 demo.py
python3 examples/live_metrics_snapshot.py
python3 examples/network_health_agent.py
python3 examples/risk_gate_agent.py
```

## Public API Expectations

- New public behavior should be exported from `hedera_ml_pipeline` and documented in `docs/LIBRARY_API.md`.
- Internal implementation should stay in `src/` and not be part of the public import surface.
- Avoid breaking changes to existing public exports without a clear migration path.

## Pull Requests

- Keep changes focused.
- Document new public behavior.
- Avoid committing generated data, local logs, private credentials, or model artifacts.
- Explain how you verified the change.
- Use the PR template checklist for validation and boundary checks.
