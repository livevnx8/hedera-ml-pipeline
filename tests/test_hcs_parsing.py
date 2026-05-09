import base64
import json

from src.metrics import HederaOnChainMetrics


class FakeHcsClient:
    async def get_topic_messages(self, topic_id: str, limit: int = 100):
        payload = {"signal": "watch", "score": 0.75}
        encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        return [
            {
                "topic_id": topic_id,
                "sequence_number": 1,
                "message": encoded,
                "consensus_timestamp": "1714953600.123456789",
            }
        ]


def test_hcs_signals_decode_base64_json():
    metrics = HederaOnChainMetrics(FakeHcsClient())

    import asyncio

    result = asyncio.run(metrics.get_hcs_signals(["0.0.12345"]))

    assert result["signal_count"] == 1
    assert result["signals"][0]["content"] == {"signal": "watch", "score": 0.75}
    assert result["signals"][0]["topic_id"] == "0.0.12345"
    assert result["signals"][0]["raw_message"]
