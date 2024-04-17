
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int
    HYPHENATERPCPORT: int
    DELIMITER: str
    EN_MODEL: str
    ES_MODEL: str
    DE_MODEL: str
    FR_MODEL: str
    NL_MODEL: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
