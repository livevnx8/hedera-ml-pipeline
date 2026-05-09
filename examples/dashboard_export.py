#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hedera_ml_pipeline import get_live_metrics


async def main():
    snapshot = await get_live_metrics()
    print(snapshot)


if __name__ == "__main__":
    asyncio.run(main())
