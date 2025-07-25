# NR5103E SDK

A Python SDK for interacting with NR5103E routers. It handles login, sessions, and basic router queries.

## Quick Start

### Installation

```sh
pip install nr5103e-sdk
```

### Usage Example

```python
import asyncio
from nr5103e_sdk.client import Client

async def main():
    async with Client("admin_password") as client:
        await client.user_login()
        status = await client.cellwan_status()
        print(f"Cell ID: {status['INTF_Cell_ID']}")

asyncio.run(main())
```

