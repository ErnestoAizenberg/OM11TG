from app import create_app
from config import Config, RedisConfig, APIURLConfig

if __name__ == "__main__":
    app_config = Config()
    api_url_config = APIURLConfig()
    app = create_app(
        app_config=app_config,
        api_url_config=api_url_config,
        redis_config=RedisConfig(),
    )
    app.run(
        debug=app_config.get("DEBUG", False),
        port=app_config.get("PORT", 5000),
        host=app_config.get("HOST", "localhost"),
    )
