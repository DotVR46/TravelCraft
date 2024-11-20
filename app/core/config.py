from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TravelCraft"
    graphql_path: str = "/graphql"


settings = Settings()
