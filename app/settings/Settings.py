from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    ALGORITHM: str
    SECRET_KEY: str
    DATABASE_PASSWORD: str
