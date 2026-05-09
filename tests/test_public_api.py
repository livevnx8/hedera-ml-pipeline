import hedera_ml_pipeline as hmp


def test_public_api_exports_core_classes():
    assert hmp.HederaMirrorNodeClient is not None
    assert hmp.HederaOnChainMetrics is not None
    assert hmp.get_live_metrics is not None
    assert hmp.KellyCriterionSizing is not None
    assert hmp.FixedFractionSizing is not None
    assert hmp.RiskManagement is not None


def test_public_api_position_sizing_smoke_test():
    sizing = hmp.KellyCriterionSizing(max_fraction=0.02)
    position = sizing.calculate(10_000, 0.25, confidence=0.55)

    assert position.size > 0
    assert position.fraction <= 0.02
