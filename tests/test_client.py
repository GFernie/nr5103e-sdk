import pytest

from nr5103e_sdk.client import Client


@pytest.mark.asyncio
async def test_client_context_manager():
    async with Client("password"):
        pass


@pytest.mark.asyncio
async def test_client_session_lazy():
    client = Client("password")
    async with client:
        assert "session" not in client.__dict__
