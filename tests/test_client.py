from nr5103e_sdk.client import Client


def test_client_context_manager():
    with Client("password"):
        pass


def test_client_session_lazy():
    client = Client("password")
    with client:
        assert "session" not in client.__dict__
