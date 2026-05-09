# Library API

A small public API is exposed through the `hedera_ml_pipeline` package so developers do not need to import from internal modules.

## Install

```bash
git clone https://github.com/livevnx8/hedera-ml-pipeline.git
cd hedera-ml-pipeline
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
```

For tests:

```bash
python3 -m pip install -e ".[dev]"
pytest
```

## Public Imports

```python
from hedera_ml_pipeline import (
    HederaMirrorNodeClient,
    HederaOnChainMetrics,
    KellyCriterionSizing,
    FixedFractionSizing,
    RiskManagement,
)
```

## Fetch Live Hedera Metrics

```python
import asyncio
from hedera_ml_pipeline import HederaMirrorNodeClient, HederaOnChainMetrics


async def main():
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)
        snapshot = await metrics.get_all_metrics()
        print(snapshot)


asyncio.run(main())
```

## Size A Position

```python
from hedera_ml_pipeline import KellyCriterionSizing

sizing = KellyCriterionSizing(max_fraction=0.02)
position = sizing.calculate(
    portfolio_value=10_000,
    current_price=0.30,
    confidence=0.55,
)

print(position.size)
print(position.fraction)
print(position.risk_amount)
```

## Apply A Risk Gate

```python
from hedera_ml_pipeline import RiskManagement

risk = RiskManagement(
    stop_loss_pct=0.01,
    take_profit_pct=0.02,
    max_daily_loss_pct=0.05,
    max_positions=5,
)

if risk.should_open_position():
    stop_loss = risk.calculate_stop_loss(0.30, "long")
    take_profit = risk.calculate_take_profit(0.30, "long")
```

## HCS Signals

```python
import asyncio
from hedera_ml_pipeline import HederaMirrorNodeClient, HederaOnChainMetrics


async def main():
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)
        signals = await metrics.get_hcs_signals(["0.0.12345"])
        print(signals)


asyncio.run(main())
```

HCS topic messages are base64-decoded before JSON/text parsing. Schema validation and chunk reconstruction are planned but not included yet.
