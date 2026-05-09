# Extending The Library

This repository is designed to stay small, readable, and easy to extend.

## Add A New Mirror Node Method

Add low-level endpoint access in `src/mirror_node.py` when the method maps directly to a Hedera Mirror Node REST endpoint.

Good fit:

- Account lookups
- Token lookups
- Topic message reads
- Network endpoints

Keep methods narrow and return the Mirror Node response shape with minimal transformation.

## Add A New Metric

Add derived metrics in `src/metrics.py` when raw Mirror Node data needs to be converted into agent-ready context.

Good fit:

- Activity summaries
- Decoded HCS signals
- Account or token concentration summaries
- Dashboard-ready metric snapshots

Keep derived metrics explicit about assumptions and sample size.

## Add A New Agent Example

Add runnable examples in `examples/` when the workflow helps builders understand how to use the library.

Good examples:

- Treasury monitor agent
- HCS signal watcher agent
- Dashboard JSON exporter
- Research feature snapshot generator

Each example should:

- Run with `python3 examples/name.py`
- Avoid private keys
- Print readable JSON or clear terminal output
- Include limitations if it uses public data samples

## Add Tests

Add offline tests in `tests/` for deterministic behavior.

Recommended test targets:

- Public imports
- Position sizing behavior
- Risk gate decisions
- HCS message decoding
- Agent report formatting

Live network calls should remain examples or optional validation, not required unit tests.

## Public API Rule

If something is meant for adopters, export it from `hedera_ml_pipeline` and document it in `docs/LIBRARY_API.md`.

If something is internal or experimental, keep it out of the public package exports until it is stable.
