import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

load_dotenv()
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")
NAME = os.getenv("DB_NAME")

BASE_DIR = Path(__file__).parent.parent


class Setting(BaseSettings):
    api_v1_prefix: str = "/api_v1/v1"

    db_url: str = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}/{NAME}"
    db_echo: bool = False
    # db_echo: bool = True


settings = Setting()
