"""
HCS message schema validation.

Defines JSON schemas for common HCS signal formats and provides validation helpers.
"""

import json
from typing import Dict, Any, Optional, List
from jsonschema import validate, ValidationError


# Common HCS signal schemas
SIGNAL_SCHEMAS = {
    "simple_signal": {
        "type": "object",
        "properties": {
            "signal": {"type": "string"},
            "score": {"type": "number", "minimum": 0, "maximum": 1},
        },
        "required": ["signal"],
        "additionalProperties": True,
    },
    "price_signal": {
        "type": "object",
        "properties": {
            "asset": {"type": "string"},
            "price": {"type": "number"},
            "timestamp": {"type": "string"},
        },
        "required": ["asset", "price"],
        "additionalProperties": True,
    },
    "health_signal": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["healthy", "degraded", "critical"]},
            "score": {"type": "number", "minimum": 0, "maximum": 100},
            "message": {"type": "string"},
        },
        "required": ["status"],
        "additionalProperties": True,
    },
}


def validate_hcs_signal(content: Any, schema_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate an HCS signal content against a schema.

    Args:
        content: The parsed content (dict or string)
        schema_name: Optional schema name to validate against

    Returns:
        Dict with:
        - valid: Boolean indicating if validation passed
        - errors: List of validation errors (if any)
        - schema_name: The schema used for validation
    """
    if not isinstance(content, dict):
        return {
            "valid": False,
            "errors": ["Content is not a JSON object"],
            "schema_name": schema_name or "none",
        }

    if schema_name and schema_name in SIGNAL_SCHEMAS:
        schema = SIGNAL_SCHEMAS[schema_name]
        try:
            validate(instance=content, schema=schema)
            return {
                "valid": True,
                "errors": [],
                "schema_name": schema_name,
            }
        except ValidationError as e:
            return {
                "valid": False,
                "errors": [str(e)],
                "schema_name": schema_name,
            }

    # If no schema specified, try to match against known schemas
    for name, schema in SIGNAL_SCHEMAS.items():
        try:
            validate(instance=content, schema=schema)
            return {
                "valid": True,
                "errors": [],
                "schema_name": name,
            }
        except ValidationError:
            continue

    return {
        "valid": True,
        "errors": [],
        "schema_name": "unknown",
    }


def get_schema_names() -> List[str]:
    """Return list of available schema names."""
    return list(SIGNAL_SCHEMAS.keys())
