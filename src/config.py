from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    MODE: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(Path.cwd(), ".env")
    )

    @property
    def psycopg_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    @property
    def asyncpg_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

settings = Settings()