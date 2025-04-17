from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)

    redis_host: str = Field("localhost")
    redis_port: int = Field(6379)
    redis_db: int = Field(0)
    redis_user: str = Field("")
    redis_password: str = Field("")

    postgres_host: str = Field("localhost")
    postgres_port: str = Field("5432")
    postgres_db: str = Field("codebase_data")
    postgres_user: str = Field("postgres")
    postgres_password: str = Field("")

    secret_code: str

    refresh_expire: int = Field(2592000)
    access_expire: int = Field(7200)

    is_dev: bool = Field(True)

    @property
    def url(self) -> str:
        return f"{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}"


settings = APISettings()
