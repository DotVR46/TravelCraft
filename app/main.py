from fastapi import FastAPI
from app.api.graphql import router as graphql_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

# Подключаем маршруты
app.include_router(graphql_router)


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.app_name}!"}
