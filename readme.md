# async-yacut

`async-yacut` - веб-сервис для сокращения ссылок с поддержкой:
- классического URL shortener (веб-форма + API);
- асинхронной загрузки файлов на Яндекс.Диск с автоматическим созданием коротких ссылок на скачивание.

## Что делает проект

- Создает короткие ссылки для любых валидных URL.
- Поддерживает пользовательский `custom_id` или автогенерацию короткого идентификатора.
- Перенаправляет по короткой ссылке на исходный URL.
- Предоставляет REST API для интеграций.
- Загружает несколько файлов на Яндекс.Диск параллельно (через `aiohttp`) и возвращает короткие ссылки на каждый файл.

## Технологии

- Python
- Flask 3
- Flask-SQLAlchemy, SQLAlchemy
- Flask-Migrate, Alembic
- Flask-WTF / WTForms
- aiohttp, asyncio
- SQLite (по умолчанию; можно использовать другую БД через `DATABASE_URI`)
- pytest

## Архитектура и ключевые модули

- `yacut/views.py` - веб-страницы (`/`, `/files`, редирект `/<short_id>`).
- `yacut/api_views.py` - API-эндпоинты (`/api/id/`, `/api/id/<short_id>/`).
- `yacut/models.py` - модель `URLMap`, генерация и хранение коротких ссылок.
- `yacut/validators.py` - валидация URL и `custom_id`.
- `yacut/yandex_disk.py` - асинхронная интеграция с API Яндекс.Диска.
- `migrations/` - миграции БД (Alembic).

## Ограничения и правила

- `custom_id` должен быть уникальным, содержать только латиницу и цифры (`A-Z`, `a-z`, `0-9`) и быть длиной до 16 символов.
- Если `custom_id` не задан, генерируется автоматически (длина 6 символов).
- Идентификатор `files` зарезервирован под страницу загрузки файлов.
- Для загрузки файлов обязателен `DISK_TOKEN` (OAuth токен Яндекс.Диска).

## Быстрый старт

### 1. Клонирование и окружение

```bash
git clone <repo_url>
cd async-yacut
python -m venv venv
```

Linux/macOS:
```bash
source venv/bin/activate
```

Windows (PowerShell):
```powershell
venv\Scripts\Activate.ps1
```

### 2. Установка зависимостей

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте `.env` в корне проекта:

```env
FLASK_APP=yacut
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
FLASK_DEBUG=1
DISK_TOKEN=
```

### 4. Миграции БД

```bash
flask db upgrade
```

### 5. Запуск

```bash
flask run
```

После запуска сервис доступен по адресу `http://127.0.0.1:5000/`.

## API

### `POST /api/id/`

Создает короткую ссылку.

Пример запроса:
```bash
curl -X POST http://127.0.0.1:5000/api/id/ \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/very/long/url","custom_id":"example1"}'
```

Пример ответа (`201 Created`):
```json
{
  "url": "https://example.com/very/long/url",
  "short_link": "http://127.0.0.1:5000/example1"
}
```

### `GET /api/id/<short_id>/`

Возвращает исходный URL по короткому идентификатору.

Пример запроса:
```bash
curl http://127.0.0.1:5000/api/id/example1/
```

Пример ответа (`200 OK`):
```json
{
  "url": "https://example.com/very/long/url"
}
```

Спецификация API: `openapi.yml`  
Postman-коллекция: `postman_collection/Yacut.postman_collection.json`

## Веб-интерфейс

- `/` - создание короткой ссылки для URL.
- `/files` - массовая загрузка файлов на Яндекс.Диск и получение коротких ссылок.
- `/<short_id>` - редирект на исходный URL.

## Тестирование

```bash
pytest
```

В проекте есть тесты для:
- API и валидации,
- веб-страниц,
- обработки ошибок,
- загрузки файлов через mock-сервер Яндекс.Диска.
