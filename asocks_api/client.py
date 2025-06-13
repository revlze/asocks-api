import os
import logging
import requests
from typing import Optional, Dict, Any, List

from dotenv import load_dotenv
from .exceptions import ASocksError, APIRequestError, AuthenticationError
from .utils import retry_on_exception


load_dotenv()
logger = logging.getLogger(__name__)


class ASocksClient:
  BASE_URL = "https://api.asocks.com/v2"

  def __init__(self, api_key: Optional[str] = None):
    self.api_key = api_key or os.getenv("ASOCKS_API_KEY")
    if not self.api_key:
      raise AuthenticationError("ASOCKS API key is not set.")
    self.session = requests.Session()

  def _request(self, method: str, endpoint: str, params: Dict[str, Any] = None) -> Any:
    url = f"{self.BASE_URL}/{endpoint}"
    params = params or {}
    params["apiKey"] = self.api_key

    try:
      response = self.session.request(method, url, params=params)
      if response.status_code == 401:
        raise AuthenticationError("Invalid API key.")
      response.raise_for_status()
      return response.json()
    except requests.HTTPError:
      raise APIRequestError(response.status_code, response.text)
    except requests.RequestException as e:
      raise ASocksError(f"Request failed: {e}")

  # --- Main Methods ---
  @retry_on_exception(max_retries=3, delay=1)
  def get_ports(self) -> List[Dict[str, Any]]:
    return self._request("GET", "proxy/ports/").get("message", {}).get("proxies", [])
  
  @retry_on_exception(max_retries=3, delay=1)
  def get_port_info(self, port_id: str) -> Dict[str, Any]:
    return self._request("GET", f"proxy/port/{port_id}")

  @retry_on_exception(max_retries=3, delay=1)
  def start_proxy(self, port_id: str) -> Dict[str, Any]:
    return self._request("POST", f"proxy/start/{port_id}")

  @retry_on_exception(max_retries=3, delay=1)
  def stop_proxy(self, port_id: str) -> Dict[str, Any]:
    return self._request("POST", f"proxy/stop/{port_id}")

  @retry_on_exception(max_retries=3, delay=1)
  def refresh_ip(self, port_id: str) -> Dict[str, Any]:
    return self._request("GET", f"proxy/refresh/{port_id}")
  
  @retry_on_exception(max_retries=3, delay=1)
  def get_proxy_status(self, port_id: str) -> Dict[str, Any]:
    return self._request("GET", f"proxy/status/{port_id}")

  @retry_on_exception(max_retries=3, delay=1)
  def get_country_list(self) -> List[Dict[str, Any]]:
    return self._request("GET", "dir/countries/").get("message", [])

  @retry_on_exception(max_retries=3, delay=1)
  def get_city_list(self, country_id: int) -> List[Dict[str, Any]]:
    return self._request("GET", "dir/cities/", params={"country": country_id}).get("message", [])

  @retry_on_exception(max_retries=3, delay=1)
  def get_state_list(self, country_id: int) -> List[Dict[str, Any]]:
    return self._request("GET", "dir/states/", params={"country": country_id}).get("message", [])

  @retry_on_exception(max_retries=3, delay=1)
  def get_isp_list(self, country_id: int) -> List[Dict[str, Any]]:
    return self._request("GET", "dir/isps/", params={"country": country_id}).get("message", [])
