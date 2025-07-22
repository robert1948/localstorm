from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List
import os

class Settings(BaseSettings):
    project_name: str = Field("CapeControl", alias="PROJECT_NAME")
    postgres_db: str = Field("capecontrol", alias="POSTGRES_DB")
    postgres_user: str = Field("capecontrol_user", alias="POSTGRES_USER")
    postgres_password: str = Field("dev-password-123", alias="POSTGRES_PASSWORD")
    secret_key: str = Field("dev-secret-key-change-in-production", alias="SECRET_KEY")
    environment: str = Field("development", alias="ENVIRONMENT")
    debug: bool = Field(True, alias="DEBUG")
    allowed_hosts: str = Field("", alias="ALLOWED_HOSTS")
    cors_origins: str = Field("", alias="CORS_ORIGINS")
    api_url: str = Field("http://localhost:8000", alias="API_URL")
    database_url: str = Field("sqlite:///./capecontrol.db", alias="DATABASE_URL")
    frontend_origin: str = Field("http://localhost:3000", alias="FRONTEND_ORIGIN")
    
    # Email configuration
    smtp_server: str = Field("localhost", alias="SMTP_SERVER")
    smtp_port: int = Field(587, alias="SMTP_PORT")
    smtp_use_tls: bool = Field(True, alias="SMTP_USE_TLS")
    smtp_username: str = Field("", alias="SMTP_USERNAME")
    smtp_password: str = Field("", alias="SMTP_PASSWORD")
    from_email: str = Field("noreply@localhost", alias="FROM_EMAIL")
    
    # S3 configuration
    aws_access_key_id: str = Field("", alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field("", alias="AWS_SECRET_ACCESS_KEY")
    aws_storage_bucket_name: str = Field("", alias="AWS_STORAGE_BUCKET_NAME")
    aws_s3_region_name: str = Field("us-east-1", alias="AWS_S3_REGION_NAME")
    
    # Session configuration
    session_secret: str = Field("dev-session-secret", alias="SESSION_SECRET")
    jwt_secret_key: str = Field("dev-jwt-secret", alias="JWT_SECRET_KEY")
    
    # Rate limiting
    rate_limit_enabled: bool = Field(False, alias="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(100, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(3600, alias="RATE_LIMIT_WINDOW")
    
    @property
    def allowed_hosts_list(self) -> List[str]:
        if isinstance(self.allowed_hosts, str):
            return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]
        return []
    
    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return []
    
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"

    @field_validator("allowed_hosts", mode="before")
    @classmethod
    def split_allowed_hosts(cls, v):
        # This validator is no longer needed but kept for compatibility
        return v or ""

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, v):
        # This validator is no longer needed but kept for compatibility
        return v or ""

    model_config = SettingsConfigDict(
        env_file=[".env.production" if os.getenv("ENVIRONMENT") == "production" else ".env"],
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()

# Production safety checks
if settings.is_production:
    if settings.secret_key == "dev-secret-key-change-in-production":
        raise ValueError("CRITICAL: Production SECRET_KEY must be changed from development default!")
    
    if settings.debug:
        print("WARNING: DEBUG is True in production environment")
    
    if not settings.database_url.startswith("postgresql://"):
        print("WARNING: Production should use PostgreSQL database")
    
    if "localhost" in settings.cors_origins_list or "127.0.0.1" in settings.cors_origins_list:
        print("WARNING: Localhost CORS origins detected in production")
    
    if not settings.allowed_hosts_list or "localhost" in settings.allowed_hosts_list:
        print("WARNING: Production ALLOWED_HOSTS should not include localhost")
