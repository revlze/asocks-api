import time
import logging
from pathlib import Path
from functools import wraps
from typing import Callable, Dict

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_env_file(env_path: str = ".env") -> None:
  """Загружает переменные окружения из .env файла."""
  env_file = Path(env_path)
  if env_file.exists():
    load_dotenv(dotenv_path=env_file)
    logger.debug(f"Loaded environment from {env_path}")
  else:
    logger.warning(f"No .env file found at {env_path}")


def is_valid_port_format(port: Dict) -> bool:
  """Проверяет наличие необходимых полей в информации о порте."""
  required_fields = {"proxy", "login", "password"}
  return required_fields.issubset(port.keys())


def format_proxy_string(proxy_dict: Dict) -> str:
  """Форматирует словарь прокси в строку вида login:password@ip:port."""
  proxy = proxy_dict.get("proxy", "")
  login = proxy_dict.get("login", "")
  password = proxy_dict.get("password", "")
  return f"{login}:{password}@{proxy}"


def retry_on_exception(
  max_retries: int = 3,
  delay: int = 2,
  exceptions: tuple = (Exception,)
) -> Callable:
  """Декоратор для повторного выполнения функции при исключениях."""
  def decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
      for attempt in range(1, max_retries + 1):
        try:
          return func(*args, **kwargs)
        except exceptions as e:
          logger.warning(f"Attempt {attempt} failed with error: {e}")
          if attempt == max_retries:
            raise
          time.sleep(delay)
    return wrapper
  return decorator
