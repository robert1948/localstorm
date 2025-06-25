from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List

class Settings(BaseSettings):
    project_name: str = Field("Tailstorm", alias="PROJECT_NAME")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    secret_key: str = Field(..., alias="SECRET_KEY")
    env: str = Field("development", alias="ENV")
    debug: bool = Field(True, alias="DEBUG")
    allowed_hosts: List[str] = Field(default_factory=list, alias="ALLOWED_HOSTS")
    cors_origins: List[str] = Field(default_factory=list, alias="CORS_ORIGINS")  # ← Add this
    api_url: str = Field(..., alias="API_URL")
    database_url: str = Field(..., alias="DATABASE_URL")

    @field_validator("allowed_hosts", mode="before")
    @classmethod
    def split_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()
