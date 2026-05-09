import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.hcs_schemas import validate_hcs_signal, get_schema_names, SIGNAL_SCHEMAS


def test_validate_simple_signal():
    content = {"signal": "watch", "score": 0.75}
    result = validate_hcs_signal(content, "simple_signal")
    assert result["valid"] is True
    assert result["schema_name"] == "simple_signal"
    assert len(result["errors"]) == 0


def test_validate_simple_signal_missing_required():
    content = {"score": 0.75}
    result = validate_hcs_signal(content, "simple_signal")
    assert result["valid"] is False
    assert result["schema_name"] == "simple_signal"
    assert len(result["errors"]) > 0


def test_validate_price_signal():
    content = {"asset": "HBAR", "price": 0.30, "timestamp": "2026-05-09"}
    result = validate_hcs_signal(content, "price_signal")
    assert result["valid"] is True
    assert result["schema_name"] == "price_signal"


def test_validate_health_signal():
    content = {"status": "healthy", "score": 95, "message": "All systems normal"}
    result = validate_hcs_signal(content, "health_signal")
    assert result["valid"] is True
    assert result["schema_name"] == "health_signal"


def test_validate_auto_detect_schema():
    content = {"signal": "buy", "score": 0.85}
    result = validate_hcs_signal(content)
    assert result["valid"] is True
    assert result["schema_name"] == "simple_signal"


def test_validate_non_dict_content():
    content = "plain text message"
    result = validate_hcs_signal(content)
    assert result["valid"] is False
    assert len(result["errors"]) > 0


def test_get_schema_names():
    names = get_schema_names()
    assert "simple_signal" in names
    assert "price_signal" in names
    assert "health_signal" in names
