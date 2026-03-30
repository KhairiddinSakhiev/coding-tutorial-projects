from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database.session import engine
from routers.user_routes import router as user_router
import uvicorn

# ВАЖНО: импортируем все модели чтобы alembic их видел
import models.user  # noqa: F401


# ─── Lifespan ─────────────────────────────────────────────────
# Код ДО yield — выполняется при запуске приложения
# Код ПОСЛЕ yield — выполняется при остановке приложения



# ─── Создание приложения ───────────────────────────────────────

app = FastAPI(
    title="Users API",
    description="Async CRUD API — FastAPI + SQLAlchemy + Pydantic + Alembic",
    version="1.0.0",
    docs_url="/docs",     # Swagger UI: http://localhost:8000/docs
    redoc_url="/redoc",   # ReDoc: http://localhost:8000/redoc
)

# ─── CORS ──────────────────────────────────────────────────────
# Разрешаем запросы с других доменов (для фронтенда)
# В продакшене укажи конкретный домен вместо "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # в продакшене: ["https://mysite.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Роутеры ──────────────────────────────────────────────────
# Подключаем роутер пользователей с префиксом /api/v1
# Все эндпоинты будут: /api/v1/users

app.include_router(user_router, prefix="/api/v1")


# ─── Health Check ──────────────────────────────────────────────
# Простой эндпоинт чтобы проверить что приложение работает
# Используется балансировщиком нагрузки и мониторингом

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "debug": settings.debug}


if __name__ == "__main__":
    uvicorn.run("manage:app", host="127.0.0.1", port=8000, reload=True)