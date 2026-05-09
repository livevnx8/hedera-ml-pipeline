# Hosted API

Optional FastAPI server that exposes Hedera metrics and risk helpers as HTTP endpoints.

## Install with API dependencies

```bash
python3 -m pip install -e ".[api]"
```

## Run the server

```bash
uvicorn examples.api_server:app --host 127.0.0.1 --port 8000
```

## Endpoints

### GET /health

Check service health.

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "ok",
  "service": "hedera-ml-pipeline-api"
}
```

### GET /metrics

Fetch live Hedera mainnet metrics.

```bash
curl http://127.0.0.1:8000/metrics
```

Response:

```json
{
  "staking": {...},
  "supply": {...},
  "transactions": {...}
}
```

### POST /risk-gate

Run a risk gate check on a proposed position.

```bash
curl -X POST http://127.0.0.1:8000/risk-gate \
  -H "Content-Type: application/json" \
  -d '{"confidence": 0.55, "portfolio_value": 10000, "current_price": 0.30}'
```

Response:

```json
{
  "allowed": true,
  "position_size": 366.67,
  "portfolio_fraction": 0.011,
  "risk_amount": 3.67
}
```

## Notes

- This API is optional and separate from the core library.
- It uses public Hedera Mirror Node endpoints.
- Do not expose this API publicly without adding authentication, rate limiting, and appropriate controls.
- This is developer tooling, not financial advice.
