"""Client for interacting with NR5103E router."""

import logging
from base64 import b64encode
from functools import cached_property
from types import TracebackType
from typing import Self
from urllib.parse import urljoin

import requests

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

    def __enter__(self) -> Self:
        """Do nothing."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Close and delete session from instance cache."""
        if "session" in self.__dict__:
            self.session.close()
            del self.__dict__["session"]
        return None

    @cached_property
    def session(self) -> requests.Session:
        """Lazy requests session."""
        session = requests.Session()
        session.verify = self.verify
        return session

    def user_login(self) -> None:
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
        response = self.session.post(url, json=body, timeout=self.timeout)
        if not response.ok:
            log.warning(
                "Unexpected response for URL %s\nStatus Code: %s\nResponse Body: %s",
                url,
                response.status_code,
                response.text,
            )

    def user_login_check(self) -> bool:
        """Check if login is valid."""
        url = urljoin(self.host, "cgi-bin/UserLoginCheck")
        response = self.session.get(url, timeout=self.timeout)
        log.info("Login status: %s", response.status_code)
        return response.ok

    def cellwan_status(self) -> dict:
        """Get info about cell interface status."""
        url = urljoin(self.host, "cgi-bin/DAL?oid=cellwan_status")
        response = self.session.get(url, timeout=self.timeout)
        return response.json()["Object"][0]
