# NR5103E SDK

A Python SDK for interacting with NR5103E routers. It handles login, sessions, and basic router queries.

## Quick Start

### Installation

```sh
pip install nr5103e-sdk
```

### Usage Example

```python
from nr5103e_sdk.client import Client

with Client("admin_password") as client:
    status = client.cellwan_status()
    print(f"Cell ID: {status['INTF_Cell_ID']")
```

