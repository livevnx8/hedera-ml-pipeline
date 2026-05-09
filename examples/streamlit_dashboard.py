#!/usr/bin/env python3
"""
Streamlit dashboard example for Hedera metrics.

Run with: streamlit run examples/streamlit_dashboard.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from hedera_ml_pipeline import get_live_metrics


@st.cache_data(ttl=60)
def fetch_metrics():
    """Fetch cached metrics (60s TTL)."""
    return asyncio.run(get_live_metrics())


st.set_page_config(page_title="Hedera Metrics Dashboard", page_icon="📊")

st.title("Hedera Metrics Dashboard")

st.sidebar.header("Controls")
refresh = st.sidebar.button("Refresh Metrics")

if refresh:
    st.cache_data.clear()

metrics = fetch_metrics()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Stake (HBAR)", f"{metrics['staking']['stake_total']:,.2f}")
    st.metric("Reward Rate", f"{metrics['staking']['staking_reward_rate']:.4f}")

with col2:
    st.metric("Circulating Supply (HBAR)", f"{metrics['supply']['released_supply']:,.2f}")
    st.metric("Circulation %", f"{metrics['supply']['circulation_pct']:.2f}%")

with col3:
    st.metric("Recent Transactions", metrics['transactions']['total_transactions'])
    st.metric("Unique Accounts", metrics['transactions']['unique_accounts'])

st.subheader("Transaction Activity")
st.write(f"Average transaction value: {metrics['transactions']['avg_transaction_value']:.4f} HBAR")

st.subheader("Raw Metrics")
st.json(metrics)
