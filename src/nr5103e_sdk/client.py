"""Client for interacting with NR5103E router."""

import logging
from base64 import b64encode
from types import TracebackType
from typing import Self
from urllib.parse import urljoin

import aiohttp

DEFAULT_HOST = "https://192.168.1.1"
DEFAULT_USERNAME = "admin"

log = logging.getLogger(__name__)


class Client:
    """Client for interacting with NR5103E router."""

    def __init__(
        self,
        *args: str,
        username: str = DEFAULT_USERNAME,
        password: str | None = None,
        host: str = DEFAULT_HOST,
        verify: bool | None = True,
    ) -> None:
        """Initialise client with some common defaults.

        Positional args can be:
        * password
        * username, password
        * username, password, host
        """
        match len(args):
            case 0:
                if password is None:
                    msg = "Foo.__init__() missing 1 required positional argument: 'password'"  # noqa:E501
                    raise TypeError(msg)
                self.username = username
                self.password = password
                self.host = host
            case 1:
                self.username = username
                self.password = args[0]
                self.host = host
            case 2:
                self.username, self.password = args
                self.host = host
            case 3:
                self.username, self.password, self.host = args
        self.verify = verify
        self.timeout = 1
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self) -> Self:
        """Open aiohttp session."""
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        connector = aiohttp.TCPConnector(
            ssl=self.verify if self.verify is not None else True
        )
        self._session = aiohttp.ClientSession(timeout=timeout, connector=connector)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Close and delete session from instance cache."""
        if self._session is not None:
            await self._session.close()
            self._session = None
        return None

    @property
    def session(self) -> aiohttp.ClientSession:
        """Return the current session."""
        if self._session is None:
            msg = "Client session not initialized"
            raise RuntimeError(msg)
        return self._session

    async def user_login(self) -> None:
        """Log in for session."""
        url = urljoin(self.host, "UserLogin")
        encoded_password = b64encode(self.password.encode()).decode()
        body = {
            "Input_Account": self.username,
            "Input_Passwd": encoded_password,
            "currLang": "en",
            "SHA512_password": False,
        }
        log.debug("Send request to URL %s\nRequest Body: %s", url, body)
        async with self.session.post(url, json=body) as response:
            if not response.ok:
                body_text = await response.text()
                log.warning(
                    (
                        "Unexpected response for URL %s\n"
                        "Status Code: %s\nResponse Body: %s"
                    ),
                    url,
                    response.status,
                    body_text,
                )

    async def user_login_check(self) -> bool:
        """Check if login is valid."""
        url = urljoin(self.host, "cgi-bin/UserLoginCheck")
        async with self.session.get(url) as response:
            log.info("Login status: %s", response.status)
            return response.ok

    async def cellwan_status(self) -> dict:
        """Get info about cell interface status."""
        url = urljoin(self.host, "cgi-bin/DAL?oid=cellwan_status")
        async with self.session.get(url) as response:
            data = await response.json()
            return data["Object"][0]
