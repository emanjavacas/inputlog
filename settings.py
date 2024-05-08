
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict, List, Any


class Language(BaseModel):
    MODEL: str
    FREQS: str

class Settings(BaseSettings):
    PORT: int
    HYPHENATERPCPORT: int
    DELIMITER: str
    NL: Language
    DE: Language
    FR: Language
    ES: Language
    EN: Language

    model_config = SettingsConfigDict(env_file="settings.toml")


settings = Settings()
