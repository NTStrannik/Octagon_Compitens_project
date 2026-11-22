from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api import books, categories
from app.db.db import engine


# Проверка подключения к БД при запуске
@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    yield


# Создание приложения
app = FastAPI(
    title="Books API",
    description="API для работы с книгами и категориями",
    version="1.0.0",
    lifespan=lifespan
)


# Подключение маршрутов
app.include_router(books.router)
app.include_router(categories.router)


# Проверка работоспособности API
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}