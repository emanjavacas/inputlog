
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int
    HYPHENATERPCPORT: int
    DELIMITER: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()