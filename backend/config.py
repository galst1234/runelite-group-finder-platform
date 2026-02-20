from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = ""
    db_port: int = 5432
    db_name: str = ""
    db_user: str = ""
    db_password: str = ""

    model_config = SettingsConfigDict(env_file=".env")

    @model_validator(mode="after")
    def check_required_db_config(self) -> "Settings":
        missing = [
            name
            for name, value in {
                "DB_HOST": self.db_host,
                "DB_NAME": self.db_name,
                "DB_USER": self.db_user,
                "DB_PASSWORD": self.db_password,
            }.items()
            if not value
        ]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        return self


settings = Settings()
