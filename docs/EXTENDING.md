# Extending

This library is designed to be extended for custom use cases while keeping the public API stable.

## Custom Metrics

You can add custom metrics by extending the `HederaOnChainMetrics` class:

```python
from hedera_ml_pipeline import HederaOnChainMetrics, HederaMirrorNodeClient
import asyncio

class CustomMetrics(HederaOnChainMetrics):
    async def get_custom_metric(self):
        # Add your custom metric logic here
        data = await self.client.get_custom_endpoint()
        return {"custom_value": data}

async def main():
    async with HederaMirrorNodeClient("mainnet") as client:
        metrics = CustomMetrics(client)
        result = await metrics.get_custom_metric()
        print(result)

asyncio.run(main())
```

## Custom HCS Schemas

You can add custom HCS signal schemas by extending the schema definitions:

```python
from src.hcs_schemas import SIGNAL_SCHEMAS

SIGNAL_SCHEMAS["my_custom_signal"] = {
    "type": "object",
    "properties": {
        "my_field": {"type": "string"},
        "my_value": {"type": "number"},
    },
    "required": ["my_field"],
    "additionalProperties": True,
}
```

## Integration with Agent Frameworks

The library can be integrated with popular agent frameworks:

- **LangChain**: See `examples/integration_langchain.py`
- **pandas**: See `examples/integration_pandas.py`
- **Custom agents**: Use the public API exports from `hedera_ml_pipeline`

## Contributing Extensions

If you build a useful extension, consider:

1. Adding an example to the `examples/` directory
2. Updating this document with your pattern
3. Submitting a PR to share it with the community

## Public API Stability

The public API in `hedera_ml_pipeline` is intended to remain stable. Internal modules in `src/` may change between versions.

When extending, prefer:
- Public API imports from `hedera_ml_pipeline`
- Composition over modification
- Adding new methods rather than changing existing ones
