#!/usr/bin/env python3
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from hedera_ml_pipeline import (
    HederaMirrorNodeClient,
    HederaOnChainMetrics,
    KellyCriterionSizing,
    RiskManagement,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Hedera ML Pipeline API",
    description="Optional hosted API for Hedera metrics and risk helpers.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "hedera-ml-pipeline-api"}


@app.get("/metrics")
async def metrics():
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = HederaOnChainMetrics(client)
        snapshot = await metrics.get_all_metrics()
        return snapshot


@app.post("/risk-gate")
async def risk_gate(request: dict):
    confidence = request.get("confidence", 0.5)
    portfolio_value = request.get("portfolio_value", 10_000)
    current_price = request.get("current_price", 0.30)

    sizing = KellyCriterionSizing(max_fraction=0.02)
    position = sizing.calculate(portfolio_value, current_price, confidence)

    risk = RiskManagement(
        stop_loss_pct=0.01,
        take_profit_pct=0.02,
        max_daily_loss_pct=0.05,
        max_positions=5,
    )

    allowed = risk.should_open_position()

    return {
        "allowed": allowed,
        "position_size": position.size,
        "portfolio_fraction": position.fraction,
        "risk_amount": position.risk_amount,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
