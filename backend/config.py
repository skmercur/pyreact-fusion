"""
Configuration Management
Handles environment variables and configuration files
"""
import os
import yaml
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=True, env="DEBUG")
    app_name: str = Field(default="PyReact Fusion", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    api_prefix: str = Field(default="/api", env="API_PREFIX")
    
    # Database
    database_type: str = Field(default="sqlite", env="DATABASE_TYPE")
    sqlite_db_path: str = Field(default="./data/app.db", env="SQLITE_DB_PATH")
    
    # PostgreSQL
    postgres_host: str = Field(default="localhost", env="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, env="POSTGRES_PORT")
    postgres_db: str = Field(default="pyreact_fusion", env="POSTGRES_DB")
    postgres_user: str = Field(default="postgres", env="POSTGRES_USER")
    postgres_password: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    
    # MySQL
    mysql_host: str = Field(default="localhost", env="MYSQL_HOST")
    mysql_port: int = Field(default=3306, env="MYSQL_PORT")
    mysql_db: str = Field(default="pyreact_fusion", env="MYSQL_DB")
    mysql_user: str = Field(default="root", env="MYSQL_USER")
    mysql_password: str = Field(default="root", env="MYSQL_PASSWORD")
    
    # MongoDB
    mongodb_host: str = Field(default="localhost", env="MONGODB_HOST")
    mongodb_port: int = Field(default=27017, env="MONGODB_PORT")
    mongodb_db: str = Field(default="pyreact_fusion", env="MONGODB_DB")
    mongodb_user: str = Field(default="", env="MONGODB_USER")
    mongodb_password: str = Field(default="", env="MONGODB_PASSWORD")
    
    # JWT
    jwt_secret_key: str = Field(default="your-secret-key-change-in-production", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:5173,http://localhost:8000",
        env="CORS_ORIGINS"
    )
    
    # Frontend
    frontend_build_path: str = Field(default="./frontend/dist", env="FRONTEND_BUILD_PATH")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", env="LOG_FILE")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment.lower() == "production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def _apply_app_config(settings_instance: Settings) -> Settings:
    """Apply app_config.json overrides to settings"""
    from backend.app_config import load_app_config
    app_config = load_app_config()
    if app_config:
        if "database" in app_config:
            settings_instance.database_type = app_config["database"].get("type", settings_instance.database_type)
        if "server" in app_config:
            server_config = app_config["server"]
            if "host" in server_config:
                settings_instance.host = server_config["host"]
            if "port" in server_config:
                settings_instance.port = server_config["port"]
    return settings_instance


def load_yaml_config(config_path: str) -> Optional[dict]:
    """Load configuration from YAML file"""
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return None


# Global settings instance
settings = Settings()
# Apply app_config.json overrides
settings = _apply_app_config(settings)

