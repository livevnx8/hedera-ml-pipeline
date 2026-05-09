# Roadmap

## Done

- Hedera Mirror Node async client
- Staking, supply, transaction, and HCS-oriented metrics
- Kelly and fixed-fraction position sizing
- Risk-management helpers
- Demo and architecture docs
- Network health agent example
- Risk gate agent example
- Hedera agent blueprint documentation
- Public library API with convenience helper
- Offline pytest suite
- Public boundary, limitations, security, support, changelog, and extension docs
- GitHub CI workflow, issue templates, and PR template

## Phase 1: Trust + Release Hardening (In Progress)

- CI workflow running pytest and syntax checks on push/PR
- README badges for CI, Python version, license, and status
- GitHub issue templates for bug reports and feature requests
- Pull request template with validation checklist
- Updated ROADMAP and CONTRIBUTING for phased direction

## Phase 2: Hedera Agent Feature Expansion (Next)

- HCS signal watcher example
- Treasury monitor example
- Dashboard JSON exporter example
- Expanded agent blueprint input/output documentation
- Offline tests for new formatting/parsing helpers

## Phase 3: Hosted API / Demo Path (Later)

- Optional FastAPI extra dependency group
- Minimal API app with `/health`, `/metrics`, `/risk-gate` endpoints
- API docs with curl examples
- Keep hosted API optional and separate from core package

## Phase 4: Profile and Ecosystem Polish (Later)

- Publish or update `livevnx8/livevnx8` profile README
- Pin `hedera-ml-pipeline` as the public Hedera tooling layer
- Add a short public launch note
- Keep QVX/Veda framed as in-house technology with future extracted tools/APIs

