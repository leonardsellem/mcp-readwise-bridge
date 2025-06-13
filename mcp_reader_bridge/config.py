from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    READWISE_TOKEN: str
    CACHE_TTL_S: int = 300           # 5 min
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
