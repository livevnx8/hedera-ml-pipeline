# Changelog

## 0.1.0

Initial public library release.

### Added

- Async Hedera Mirror Node client.
- Hedera on-chain metrics aggregation.
- HCS message decoding into agent-ready signal records.
- Kelly and fixed-fraction position sizing helpers.
- Risk-management helpers for stop-loss, take-profit, daily loss, and max-position gates.
- Public `hedera_ml_pipeline` import surface.
- `get_live_metrics()` convenience helper.
- Live demo and runnable examples.
- Offline pytest suite for core deterministic behavior.
- Public boundary, validation, limitations, security, and extension docs.

### Notes

- This release uses public Mirror Node data only.
- Private keys, wallet flows, and autonomous execution are intentionally out of scope.
- HCS schema validation and chunk reconstruction are planned future work.
