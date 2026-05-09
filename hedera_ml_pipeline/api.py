from src.metrics import HederaOnChainMetrics
from src.mirror_node import HederaMirrorNodeClient
from src.position_sizing import FixedFractionSizing, KellyCriterionSizing, PositionSize
from src.risk_management import RiskManagement


async def get_live_metrics(network: str = "mainnet", hcs_topic_ids: list[str] | None = None) -> dict:
    async with HederaMirrorNodeClient(network) as client:
        metrics = HederaOnChainMetrics(client)
        return await metrics.get_all_metrics(hcs_topic_ids=hcs_topic_ids)


__all__ = [
    "FixedFractionSizing",
    "get_live_metrics",
    "HederaMirrorNodeClient",
    "HederaOnChainMetrics",
    "KellyCriterionSizing",
    "PositionSize",
    "RiskManagement",
]
