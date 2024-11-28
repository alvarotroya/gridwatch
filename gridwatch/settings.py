from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_host: str
    db_user: str
    db_password: str
    db_name: str
    db_port: int


# make the settings object importable in other modules
app_settings = Settings()
