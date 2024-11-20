import os
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")
NAME = os.getenv("DB_NAME")


class Settings:
    # URL подключения к базе данных (замени на свой)
    database_url: str = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}/{NAME}"


settings = Settings()
