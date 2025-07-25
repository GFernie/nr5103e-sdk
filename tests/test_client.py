import base64
import inspect
from unittest.mock import patch

import aiohttp
import aioresponses
import pytest
from aiohttp import ClientError

from nr5103e_sdk.client import Client


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test that client can be used as async context manager."""
    async with Client("password"):
        pass


@pytest.mark.asyncio
async def test_client_session_lazy():
    """Test that session is created lazily."""
    client = Client("password")
    async with client:
        # Verify session is None before accessing
        assert client._session is None
        # Access session through public property to ensure lazy initialisation works
        session = client.session
        assert session is not None


@pytest.mark.asyncio
async def test_async_methods_are_coroutines():
    """Test that all the main methods are async coroutines."""
    client = Client("password")
    async with client:
        assert inspect.iscoroutinefunction(client.user_login)
        assert inspect.iscoroutinefunction(client.user_login_check)
        assert inspect.iscoroutinefunction(client.cellwan_status)


@pytest.mark.asyncio
async def test_user_login_success():
    """Test successful user login."""
    with aioresponses.aioresponses() as mock:
        mock.post("https://192.168.1.1/UserLogin", status=200)

        async with Client("test_password") as client:
            await client.user_login()

        # Verify the request was made with correct parameters
        history = mock.requests
        assert len(history) == 1

        # Check the first (and only) request
        request_key = next(iter(history.keys()))
        assert request_key[0] == "POST"
        assert str(request_key[1]) == "https://192.168.1.1/UserLogin"

        # Check the request data
        request_call = history[request_key][0]
        request_kwargs = request_call.kwargs
        request_data = request_kwargs["json"]

        assert request_data["Input_Account"] == "admin"
        assert request_data["currLang"] == "en"
        assert request_data["SHA512_password"] is False
        # Password should be base64 encoded
        expected_password = base64.b64encode(b"test_password").decode()
        assert request_data["Input_Passwd"] == expected_password


@pytest.mark.asyncio
async def test_user_login_failure():
    """Test user login with HTTP error."""
    with aioresponses.aioresponses() as mock:
        mock.post("https://192.168.1.1/UserLogin", status=401, body="Unauthorized")

        async with Client("wrong_password") as client:
            # Should not raise exception, but logs warning
            with patch("nr5103e_sdk.client.log.warning") as mock_log:
                await client.user_login()
                mock_log.assert_called_once()


@pytest.mark.asyncio
async def test_user_login_check_success():
    """Test successful login check."""
    with aioresponses.aioresponses() as mock:
        mock.get("https://192.168.1.1/cgi-bin/UserLoginCheck", status=200)

        async with Client("password") as client:
            result = await client.user_login_check()
            assert result is True


@pytest.mark.asyncio
async def test_user_login_check_failure():
    """Test failed login check."""
    with aioresponses.aioresponses() as mock:
        mock.get("https://192.168.1.1/cgi-bin/UserLoginCheck", status=401)

        async with Client("password") as client:
            result = await client.user_login_check()
            assert result is False


@pytest.mark.asyncio
async def test_cellwan_status_success():
    """Test successful cellwan status retrieval."""
    expected_data = {
        "Object": [
            {
                "INTF_Cell_ID": "12345",
                "INTF_RSRP": -85,
                "INTF_RSRQ": -10,
                "status": "connected",
            }
        ]
    }

    with aioresponses.aioresponses() as mock:
        mock.get(
            "https://192.168.1.1/cgi-bin/DAL?oid=cellwan_status",
            status=200,
            payload=expected_data,
        )

        async with Client("password") as client:
            result = await client.cellwan_status()
            assert result == expected_data["Object"][0]


@pytest.mark.asyncio
async def test_cellwan_status_http_error():
    """Test cellwan status with HTTP error."""
    with aioresponses.aioresponses() as mock:
        mock.get(
            "https://192.168.1.1/cgi-bin/DAL?oid=cellwan_status",
            status=500,
            body="Internal Server Error",
        )

        async with Client("password") as client:
            with pytest.raises(aiohttp.ClientResponseError):
                await client.cellwan_status()


@pytest.mark.asyncio
async def test_client_with_custom_parameters():
    """Test client initialisation with custom parameters."""
    client = Client("custom_user", "custom_pass", "https://192.168.2.1", verify=False)

    assert client.username == "custom_user"
    assert client.password == "custom_pass"
    assert client.host == "https://192.168.2.1"
    assert client.verify is False


@pytest.mark.asyncio
async def test_session_cleanup():
    """Test that session is properly cleaned up."""
    client = Client("password")

    async with client:
        session = client.session
        assert session is not None
        assert not session.closed

    # Session should be closed after context exit
    assert session.closed


@pytest.mark.asyncio
async def test_network_error_handling():
    """Test handling of network connectivity errors."""
    with aioresponses.aioresponses() as mock:
        mock.get(
            "https://192.168.1.1/cgi-bin/UserLoginCheck",
            exception=ClientError("Network error"),
        )

        async with Client("password") as client:
            with pytest.raises(ClientError):
                await client.user_login_check()


@pytest.mark.asyncio
async def test_ssl_verification_disabled():
    """Test that SSL verification can be disabled."""
    client = Client("password", verify=False)

    async with client:
        # Check that connector has SSL verification disabled
        connector = client.session.connector
        # aiohttp TCPConnector uses _ssl attribute to store SSL context
        assert connector._ssl is False


@pytest.mark.asyncio
async def test_ssl_verification_enabled():
    """Test that SSL verification is enabled by default."""
    client = Client("password", verify=True)

    async with client:
        # Check that connector has SSL verification enabled
        connector = client.session.connector
        # When verify=True, SSL defaults to True (uses default SSL verification)
        assert connector._ssl is True


@pytest.mark.asyncio
async def test_complete_workflow():
    """Test a complete workflow: login, check, get status."""
    cellwan_data = {
        "Object": [
            {
                "INTF_Cell_ID": "54321",
                "INTF_RSRP": -75,
                "INTF_RSRQ": -8,
                "status": "connected",
            }
        ]
    }

    with aioresponses.aioresponses() as mock:
        mock.post("https://192.168.1.1/UserLogin", status=200)
        mock.get("https://192.168.1.1/cgi-bin/UserLoginCheck", status=200)
        mock.get(
            "https://192.168.1.1/cgi-bin/DAL?oid=cellwan_status",
            status=200,
            payload=cellwan_data,
        )

        async with Client("password") as client:
            # Complete workflow
            await client.user_login()
            login_valid = await client.user_login_check()
            status = await client.cellwan_status()

            assert login_valid is True
            assert status["INTF_Cell_ID"] == "54321"
            assert status["status"] == "connected"
