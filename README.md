# asocks-api

Python-клиент для взаимодействия с [asocks.com API](https://asocks.com/).  
Позволяет управлять прокси: запуск, остановка, обновление IP, получение списка стран, городов, провайдеров и т.д.

## Установка

```bash
git clone https://github.com/revlze/asocks-api.git
cd asocks-api
cp .env.example .env # Вставьте ваш API-key в соотвествующее поле в .env
python -m venv venv
source venv/bin/activate  # или .\venv\Scripts\activate на Windows
pip install -r requirements.txt
```
