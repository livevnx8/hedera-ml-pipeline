import pytest

from hedera_ml_pipeline import HederaMirrorNodeClient


def test_mirror_node_rejects_unknown_network():
    with pytest.raises(ValueError):
        HederaMirrorNodeClient("invalid-network")


def test_mirror_node_sets_known_network_base_url():
    client = HederaMirrorNodeClient("testnet")

    assert client.network == "testnet"
    assert "testnet" in client.base_url
