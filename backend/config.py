from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env", "../.env"],
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_db: str = "leaflink"
    postgres_user: str = "leaflink"
    postgres_password: str
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 7

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
