from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str       # URL для подключения к базе данных
    secret_key: str         # секретный ключ
    debug: bool = False  
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()