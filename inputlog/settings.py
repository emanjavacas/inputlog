
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings import PydanticBaseSettingsSource, TomlConfigSettingsSource
from typing import List, Type, Tuple, Optional

import logging
import logging.config

import toml


def setup_logger(path='settings_logger.toml'):
    with open(path) as f:
        config = toml.load(f)
        logging.config.dictConfig(config)


class Language(BaseModel):
    language: str = Field(description="Language code")
    model: str = Field(default='spacy', description="Type of model")
    freqs_path: str = Field(description="Path to the frequency file")
    model_path: str = Field(description="Path to the model")
    constituency: Optional[str] = Field(default=None, description="Type of constituency model")
    constituency_path: Optional[str] = Field(default=None, description="Path to the constituency model")


class Settings(BaseSettings):
    port: int = Field(default=8000, description="Port where the app will be running")
    hyphenate_rpc_port: int = Field(default=8082, description="Port where the hyphenation system will be running")
    delimiter: str = Field(default="#-#", description="Delimiter to use for hyphenation")
    languages: List[Language] = Field(description="Language-specific configuration")
    needs_language_detection: bool = Field(default=True)
    default_language: Optional[str] = Field(default=None)
    # source file
    model_config = SettingsConfigDict(toml_file=("settings.toml"))

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)


settings = Settings()
if len(settings.languages) == 1:
    settings.needs_language_detection = False
    settings.default_language = settings.languages[0].language
