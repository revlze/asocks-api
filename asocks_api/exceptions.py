class ASocksError(Exception):
  """Базовое исключение клиента ASocks."""
  pass

class AuthenticationError(ASocksError):
  """Ошибка аутентификации (неверный или отсутствующий ключ API)."""
  pass

class APIRequestError(ASocksError):
  """Ошибка HTTP-запроса к API."""
  def __init__(self, status_code: int, message: str = ""):
    self.status_code = status_code
    self.message = message or f"API returned status code {status_code}"
    super().__init__(self.message)
