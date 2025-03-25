from pydantic_settings import BaseSettings, SettingsConfigDict



class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class Config(CustomBaseSettings):
    STORAGE_HOST: str
    STORAGE_PORT: str
    STORAGE_ACCESS_KEY: str
    STORAGE_SECRET_KEY: str
    STORAGE_BUCKET: str


settings = Config()
