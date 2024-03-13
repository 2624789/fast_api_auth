from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn


class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_name: str
    database_host: str
    database_port: int

    @property
    def database_url(self) -> PostgresDsn:
        return (f'postgresql+psycopg2://{self.database_user}'
                f':{self.database_password}@{self.database_host}'
                f':{self.database_port}/{self.database_name}')

    model_config = SettingsConfigDict(
        env_file='../.env', env_file_encoding='utf-8'
    )

settings = Settings()
