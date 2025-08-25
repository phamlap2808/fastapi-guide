# FastAPI Guide

## Chạy nhanh

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
fastapi dev app/main.py
```

- Healthcheck: `GET /health`
- Ping: `GET /api/v1/ping/`

## Cấu hình

Sao chép `.env.example` thành `.env` và chỉnh sửa tuỳ ý.

## PostgreSQL bằng Docker Compose

```bash
docker compose up -d
```

Biến môi trường mẫu (tạo `.env` từ `.env.example`):

```
APP_ENV=dev
APP_DEBUG=true
APP_DATABASE_URL=postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi
```

## Cấu trúc thư mục

```
app/
  api/
    v1/
      endpoints/
        ping.py
      router.py
  core/
    config.py
  db/
    session.py
  models/
  schemas/
  services/
  main.py
```
