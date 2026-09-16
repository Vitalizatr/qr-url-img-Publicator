# QR Code API

Лёгкий FastAPI-сервис, который умеет:
- генерировать QR-код по ссылке;
- загружать результат в ImgBB;
- принимать URL картинки и превращать её в QR-код.

Проект сделан как маленький API для быстрой генерации QR-кодов и публикации их в облаке.

## Что внутри

- `endpoints.py` — API-эндпоинты
- `services/qr_coder.py` — генерация QR-кода
- `services/img_to_url.py` — загрузка QR-картинки в ImgBB
- `.env` — переменные окружения

## Технологии

- Python 3
- FastAPI
- httpx
- qrcode
- ImgBB API

## Установка

1. Склонируй проект:

```bash
git clone <ссылка-на-репозиторий>
cd Qr-code-API
```

2. Создай виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Установи зависимости:

```bash
pip install fastapi uvicorn httpx qrcode python-dotenv
```

4. Создай файл `.env` в корне проекта и добавь ключ ImgBB:

```env
IMGBB_API_KEY=твоя_ключ_от_imgbb
```

> Ключ можно получить на сайте ImgBB в личном кабинете.

## Запуск

Запуск локального сервера:

```bash
uvicorn endpoints:app --reload
```

После этого API будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Эндпоинты

### 1) Создать QR по ссылке

`POST /url/`

Параметры:
- `url` — ссылка, которую нужно превратить в QR-код

Пример запроса:

```bash
curl -X POST "http://127.0.0.1:8000/url/?url=https://example.com"
```

Что возвращает:
- JSON-ответ от ImgBB с данными о загруженной картинке

### 2) Создать QR по ссылке на изображение

`POST /img/`

Параметры:
- `img` — ссылка на картинку

Пример:

```bash
curl -X POST "http://127.0.0.1:8000/img/?img=https://example.com/image.jpg"
```

Что возвращает:
- объект вида:

```json
{
  "qr": "<base64-строка-с-изображением-qr>"
}
```

## Как это работает по шагам

### `/url/`

1. Принимает ссылку `url`
2. Генерирует QR-код
3. Загружает изображение в ImgBB
4. Возвращает JSON от ImgBB

### `/img/`

1. Принимает ссылку на изображение `img`
2. Загружает её в ImgBB
3. Берёт URL загруженной картинки
4. Генерирует QR-код от этого URL
5. Возвращает base64-картинку QR

## Пример на Python

```python
import httpx

async def create_qr():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/url/",
            params={"url": "https://example.com"},
        )
        print(response.status_code)
        print(response.json())
```

## Возможные ошибки

- `500` — внутренняя ошибка сервера
- `HTTPStatusError` — ошибка при обращении к ImgBB
- `ValueError` — передан пустой или слишком длинный URL

## Полезные заметки

- Ссылка в `url` ограничена по длине в сервисе генерации QR.
- Если ImgBB не отвечает или ключ некорректный, запрос упадёт с ошибкой.
- Для локальной разработки удобно использовать `--reload`, чтобы сервер пересоздавался при изменениях.

## Пример структуры проекта

```text
Qr-code-API/
├── endpoints.py
├── schema.py
├── .env
├── README.md
├── services/
│   ├── img_to_url.py
│   └── qr_coder.py
└── .venv/
```

## Если хочешь дальше

Можно ещё добавить:
- загрузку файла через multipart/form-data;
- сохранение QR-кода локально на диск;
- поддержку нескольких форматов изображений;
- отдельный health check endpoint.

Если хочешь, я могу сразу сделать и второй README в более "премиум" стиле — с красивым описанием, секциями и примерами для продакшна.

