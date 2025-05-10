from app import create_app
from config import Config, RedisConfig

if __name__ == "__main__":
    app = create_app(
        app_config=Config(),
        redis_config=RedisConfig(),
    )
    app.run(
        debug=app.state_config.get("DEBUG", False),
        port=app.state_config.get("PORT", 5000),
    )
