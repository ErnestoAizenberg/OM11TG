import os
from dotenv import load_dotenv
from typing import Any, Optional, TypeVar

# Load environment variables
load_dotenv("instance/.env")

T = TypeVar('T')

def get_env(key: str, required: bool = True, default: Optional[T] = None) -> Optional[T]:
    """Safely get environment variable with optional requirement check."""
    value = os.getenv(key)
    if required and value is None and default is None:
        raise ValueError(f"Required environment variable {key} is not set")
    return value if value is not None else default


class APIURLConfig:
    """API URL configurations loaded from environment."""

    OM11: str = get_env("API_OM11_URL")
    OM11TG: str = get_env("API_OM11TG_URL")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value by key with optional default."""
        try:
            return getattr(self, key)
        except AttributeError:
            if default is not None:
                return default
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")


class Config:
    """Flask application configuration."""

    SECRET_KEY: str = get_env("SECRET_KEY")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "t")
    ENV: str = get_env("FLASK_ENV", "production")

    # Server config
    HOST: str = get_env("SERVER_HOST")
    PORT: int = int(get_env("SERVER_PORT"))
    SERVER_ADDRESS: str = get_env("SERVER_ADDRESS")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value by key with optional default.

        Args:
            key: Configuration key to retrieve
            default: Default value if key doesn't exist

        Returns:
            The configuration value or default if provided

        Raises:
            AttributeError: If key doesn't exist and no default provided
        """
        try:
            return getattr(self, key)
        except AttributeError as e:
            if default is not None:
                return default
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'") from e


class RedisConfig:
    """Redis configuration."""

    HOST: str = get_env("REDIS_HOST")
    PORT: int = int(get_env("REDIS_PORT"))
    DB: int = int(get_env("REDIS_DB"))
    DECODE_RESPONSES: bool = True

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get Redis configuration value by key.

        Example:
            >>> redis_config.get('HOST', 'localhost')
            'redis-server'
        """
        try:
            return getattr(self, key)
        except AttributeError:
            if default is not None:
                return default
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")


# Configuration instances for easy import
api_url_config = APIURLConfig()
config = Config()
redis_config = RedisConfig()
