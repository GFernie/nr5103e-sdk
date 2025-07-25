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
        # Access session through public property to ensure lazy initialization works
        session = client.session
        assert session is not None


@pytest.mark.asyncio
async def test_async_methods_are_coroutines():
    """Test that all the main methods are now async coroutines."""
    import inspect

    client = Client("password")
    async with client:
        # Check that the methods are coroutine functions
        assert inspect.iscoroutinefunction(client.user_login)
        assert inspect.iscoroutinefunction(client.user_login_check)
        assert inspect.iscoroutinefunction(client.cellwan_status)
