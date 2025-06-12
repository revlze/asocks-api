import pytest
from unittest.mock import patch
from asocks_api.client import ASocksClient

@pytest.fixture
def client():
  return ASocksClient(api_key="testkey")


@patch("asocks_api.client.requests.Session.request")
def test_get_port_info(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": {"id": "123"}}
  result = client.get_port_info("123")
  assert result["message"]["id"] == "123"


@patch("asocks_api.client.requests.Session.request")
def test_start_proxy(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": "started"}
  result = client.start_proxy("123")
  assert result["message"] == "started"


@patch("asocks_api.client.requests.Session.request")
def test_stop_proxy(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": "stopped"}
  result = client.stop_proxy("123")
  assert result["message"] == "stopped"


@patch("asocks_api.client.requests.Session.request")
def test_get_proxy_status(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": {"status": "active"}}
  result = client.get_proxy_status("123")
  assert result["message"]["status"] == "active"


@patch("asocks_api.client.requests.Session.request")
def test_get_country_list(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": [{"id": 1, "name": "USA"}]}
  result = client.get_country_list()
  assert isinstance(result, list)
  assert result[0]["name"] == "USA"


@patch("asocks_api.client.requests.Session.request")
def test_get_state_list(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": [{"id": 1, "name": "California"}]}
  result = client.get_state_list(country_id=1)
  assert isinstance(result, list)
  assert result[0]["name"] == "California"


@patch("asocks_api.client.requests.Session.request")
def test_get_isp_list(mock_request, client):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": [{"id": 1, "name": "AT&T"}]}
  result = client.get_isp_list(country_id=1)
  assert isinstance(result, list)
  assert result[0]["name"] == "AT&T"
  
@patch("asocks_api.client.requests.Session.request")
def test_get_ports_success(mock_request):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {
    "message": {
      "proxies": [{"proxy": "1.2.3.4:1234", "login": "u", "password": "p"}]
    }
  }

  client = ASocksClient(api_key="testkey")
  ports = client.get_ports()
  assert isinstance(ports, list)
  assert "proxy" in ports[0]

@patch("asocks_api.client.requests.Session.request")
def test_refresh_ip(mock_request):
  mock_request.return_value.status_code = 200
  mock_request.return_value.json.return_value = {"message": {"ip": "1.2.3.4"}}
  
  client = ASocksClient(api_key="testkey")
  data = client.refresh_ip("123")
  assert "ip" in data["message"]