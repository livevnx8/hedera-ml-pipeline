# Research Findings

Key discoveries from our Hedera ML pipeline research and development.

## 1. Data Leakage Is Pervasive

We discovered and fixed **three major data leakage sources** that caused models to report false 100% accuracy:

### Leak #1: Forward Return Calculation Bug
The forward return in `fetch_multi.py` was calculating the current candle's own return instead of the actual forward price change.

```python
# BUG: (close - open) / open of the SAME candle
ret[i] = (c[i] - o[i]) / o[i] * 10000

# FIX: Actual forward price change
ret[i] = (c[i + h_idx] - c[i]) / c[i] * 10000
```

**Impact:** Model learned to predict a candle's shape, not future price movement.

### Leak #2: binary_label as Input Feature
The `binary_label` field (the target!) was being passed as an input feature at index 9.

```python
# BUG: Only excluded keys starting with "label"
feature_keys = [k for k in row.keys() if not k.startswith("label") ...]

# FIX: Explicitly exclude "binary_label"
feature_keys = [k for k in row.keys() if ... k != "binary_label"]
```

**Impact:** Model was literally trained on the answer. Accuracy dropped from 100% → 48.8%.

### Leak #3: Balanced Sampling Memorization
Oversampling minority classes caused the model to memorize training samples rather than learn patterns.

**Fix:** Disabled balanced sampling. Train samples: 3,968 (natural distribution).

## 2. ~50% Accuracy Is the Honest Baseline

After fixing all leakage, we tested multiple approaches:

| Approach | Accuracy | Down Acc | Up Acc | Verdict |
|----------|----------|----------|--------|---------|
| Single model (large, 50k steps) | 49.3% | 85.1% | 16.3% | Strong down bias |
| Single model (xlarge, 50k steps) | 52.5% | 27.7% | 75.4% | Strong up bias |
| Single model (xlarge, 100k steps) | 51.8% | 74.6% | 30.8% | Strong down bias |
| Twin specialists | 48.7% | — | — | Extreme bias |
| Ensemble (5 models, majority) | 52.9% | 29.2% | 74.8% | Still biased |

**Conclusion:** No approach exceeded ~53% accuracy. All showed strong class bias.

## 3. Technical Indicators Don't Work

Features tested: RSI, MACD, Bollinger Bands, volume profile.

**Why they fail:**
- These are widely known, publicly available indicators
- Market participants have already priced them in
- Random walk markets are inherently unpredictable with lagging indicators
- Any edge from these indicators is arbitraged away instantly

**Evidence:** After fixing leakage, models with these features performed at chance level (48-53%).

## 4. Ensemble Methods Don't Help

We tested majority voting with 5 diverse models (different random seeds):

| Model | Accuracy |
|-------|----------|
| Model 1 (seed=42) | 52.7% |
| Model 2 (seed=52) | 52.4% |
| Model 3 (seed=62) | 53.3% |
| Model 4 (seed=72) | 53.5% |
| Model 5 (seed=82) | 52.7% |
| **Ensemble (majority)** | **52.9%** |

**Finding:** Ensemble accuracy (52.9%) ≈ individual model average (52.9%). No bias reduction.

## 5. Execution Quality > Prediction Accuracy

This is our most important finding. With ~50% model accuracy:

- **Position sizing** determines survival — Kelly Criterion prevents ruin even with coin-flip accuracy
- **Risk management** limits downside — 1% stop-loss, 5% daily loss cap
- **Execution discipline** matters more than signal quality

A system with 50% accuracy and excellent risk management outperforms a system with 55% accuracy and poor risk management over any meaningful time horizon.

## 6. Hedera On-Chain Data Is Untapped Alpha

Hedera provides unique data sources unavailable on other chains:

| Data Source | Trading Signal Potential |
|------------|------------------------|
| Staking metrics | Network confidence indicator |
| Supply changes | Inflation/deflation pressure |
| HCS topic activity | Real-time event streams |
| Token transfer volume | On-chain capital flows |
| Account creation rate | Network adoption velocity |

**Hypothesis:** These metrics may provide predictive signal because:
- They are NOT widely used in trading models (unlike RSI/MACD)
- They reflect actual network usage, not just price action
- They are unique to Hedera's architecture (HCS, native staking)

**Status:** Integration built. Awaiting feature importance testing.

## Key Takeaways

1. **Always verify your data pipeline.** Three separate leakage sources produced false 100% accuracy.
2. **Accept honest baselines.** 50% accuracy on random-walk markets is expected and acceptable.
3. **Focus on what you can control.** Position sizing and risk management matter more than prediction.
4. **Look for unique data.** Hedera's on-chain metrics are an unexplored alpha source.
5. **Ensemble methods aren't magic.** They don't fix fundamentally uninformative features.
