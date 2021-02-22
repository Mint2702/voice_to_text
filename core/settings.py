from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    common_words: str = Field(..., env="COMMON")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(_env_file="../.env")
