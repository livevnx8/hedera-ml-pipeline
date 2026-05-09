#!/usr/bin/env python3
"""
Example integration with LangChain for AI agents.

Shows how to use Hedera metrics as context for LangChain agents.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hedera_ml_pipeline import get_live_metrics


async def main():
    metrics = await get_live_metrics()

    # Format metrics as context for an LLM
    context = f"""
Current Hedera Network State:

Staking:
- Total staked: {metrics['staking']['stake_total']:.2f} HBAR
- Reward rate: {metrics['staking']['staking_reward_rate']:.4f}

Supply:
- Circulating: {metrics['supply']['released_supply']:.2f} HBAR
- Circulation %: {metrics['supply']['circulation_pct']:.2f}%

Transactions:
- Recent count: {metrics['transactions']['total_transactions']}
- Unique accounts: {metrics['transactions']['unique_accounts']}
"""

    print("=== LangChain Context ===")
    print(context)

    # Example: This context can be passed to a LangChain agent
    # from langchain.agents import initialize_agent, Tool
    # from langchain.llms import OpenAI
    #
    # llm = OpenAI(temperature=0)
    # tools = [...]
    # agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
    # result = agent.run(f"Analyze this network state: {context}")


if __name__ == "__main__":
    asyncio.run(main())
