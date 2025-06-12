from asocks_api.exceptions import AuthenticationError, APIRequestError
from asocks_api.client import ASocksClient
from unittest.mock import patch, MagicMock
import requests
import pytest


def test_authentication_error_raised(monkeypatch):
  monkeypatch.delenv("ASOCKS_API_KEY", raising=False)
  with pytest.raises(AuthenticationError):
    ASocksClient()

def test_authentication_error_no_key(monkeypatch):
  monkeypatch.delenv("ASOCKS_API_KEY", raising=False)
  with pytest.raises(AuthenticationError):
    ASocksClient(api_key=None)


@patch("asocks_api.client.requests.Session.request")
def test_api_request_error_handling(mock_request):
  mock_response = MagicMock()
  mock_response.status_code = 400
  mock_response.text = "Bad Request"
  mock_response.raise_for_status.side_effect = requests.HTTPError("Bad Request")

  mock_request.return_value = mock_response

  client = ASocksClient(api_key="testkey")
  with pytest.raises(APIRequestError) as excinfo:
    client.get_ports()

  assert excinfo.value.status_code == 400
  assert "Bad Request" in str(excinfo.value)


def test_api_request_error_object():
  err = APIRequestError(404, "Not found")
  assert err.status_code == 404
  assert "Not found" in str(err)
