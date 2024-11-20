import os

from pydantic.v1 import BaseSettings
from dotenv import load_dotenv, dotenv_values

load_dotenv()
env_config = dotenv_values(".env")


class Settings(BaseSettings):
    app_name: str = "TravelCraft"
    graphql_path: str = "/graphql"
    database_url: str = (
        f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )


settings = Settings()
