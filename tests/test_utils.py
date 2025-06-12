import pytest
import os
from pathlib import Path
from asocks_api.utils import is_valid_port_format, format_proxy_string, load_env_file, retry_on_exception

def test_is_valid_port_format_valid():
  port = {
    "proxy": "1.2.3.4:1234",
    "login": "user",
    "password": "pass"
  }
  assert is_valid_port_format(port) is True

def test_is_valid_port_format_invalid():
  port = {
    "proxy": "1.2.3.4:1234",
    "login": "user"
  }
  assert is_valid_port_format(port) is False

def test_format_proxy_string():
  port = {
    "proxy": "1.2.3.4:1234",
    "login": "user",
    "password": "pass"
  }
  expected = "user:pass@1.2.3.4:1234"
  assert format_proxy_string(port) == expected
  
def test_load_env_file(tmp_path, monkeypatch):
  env_file = tmp_path / ".env"
  env_file.write_text("MY_TEST_KEY=123")
  monkeypatch.chdir(tmp_path)
  
  load_env_file()
  
  assert os.getenv("MY_TEST_KEY") == "123"


def test_retry_on_exception_success():
  call_counter = {"count": 0}
  
  @retry_on_exception(max_retries=3, delay=0)
  def flaky_func():
    call_counter["count"] += 1
    if call_counter["count"] < 2:
      raise ValueError("fail once")
    return "ok"

  assert flaky_func() == "ok"

