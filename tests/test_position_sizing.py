from src.position_sizing import FixedFractionSizing, KellyCriterionSizing


def test_kelly_position_sizing_respects_max_fraction():
    sizing = KellyCriterionSizing(max_fraction=0.02)

    result = sizing.calculate(
        portfolio_value=10_000,
        current_price=0.25,
        confidence=0.75,
    )

    assert result.fraction <= 0.02
    assert result.size > 0
    assert result.risk_amount > 0


def test_fixed_fraction_confidence_changes_size():
    sizing = FixedFractionSizing(base_fraction=0.01)

    low = sizing.calculate(10_000, 0.25, confidence=0.3)
    high = sizing.calculate(10_000, 0.25, confidence=0.8)

    assert high.fraction > low.fraction
    assert high.size > low.size
