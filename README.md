# NR5103E SDK

A Python SDK for interacting with NR5103E routers. It handles login, sessions, and basic router queries.

## Quick Start

### Installation

```sh
pip install .
```

### Usage Example

```python
from nr5103e_sdk.client import Client
import asyncio


async def main() -> None:
    async with Client("admin_password") as client:
        status = await client.cellwan_status()
        print(f"Cell ID: {status['INTF_Cell_ID']}")


asyncio.run(main())
```

## Contributing

### Run Tests

```sh
bin/test
```

### Format Code

```sh
bin/format
```
