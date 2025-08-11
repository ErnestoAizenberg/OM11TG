import os
import subprocess
import sys
import socket

from app import create_app
from app.logs import logger
from config import Config, RedisConfig, APIURLConfig

def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

def old_main():
    # Initialize configuration objects
    app_config = Config()
    redis_config = RedisConfig()
    api_url_config = APIURLConfig()

    # Create the Flask app with provided configurations
    app = create_app(
        app_config=app_config,
        api_url_config=api_url_config,
        redis_config=redis_config,
    )

    # Determine whether to run Redis server based on environment variable
    redis_run = os.getenv("REDIS_RUN", "true").lower() == "true"

    redis_port = redis_config.get("PORT")

    if redis_run:
        if is_port_in_use(redis_port):
            logger.warning(f"Redis port {redis_port} is already in use. Assuming Redis is running.")
        else:
            print("Attempting to start Redis server...")
            try:
                subprocess.run(
                    ["redis-server", "--daemonize", "yes"],
                    check=True
                )
                print("Redis server started successfully.")
            except PermissionError:
                print(
                    "Permission denied: Unable to start redis-server. "
                    "Make sure Redis is installed and you have the necessary permissions. "
                    "You can install Redis with: sudo apt install redis-server "
                    "or pkg install redis."
                )
                sys.exit(1)
            except FileNotFoundError:
                print(
                    "redis-server command not found. Please ensure Redis is installed and accessible in your PATH."
                )
                sys.exit(1)
            except subprocess.CalledProcessError as e:
                print(f"Failed to start Redis server: {e}")
                sys.exit(1)

    # Run the Flask application
    app.run(
        debug=app_config.get("DEBUG", False),
        port=app_config.get("PORT", 5000),
        host=app_config.get("HOST", "localhost")
    )

def new_main():
    app_config = Config()
    redis_config = RedisConfig()
    api_url_config = APIURLConfig()

    app = create_app(
        app_config=app_config,
        api_url_config=api_url_config,
    )

    app.run(
        debug=app_config.get("DEBUG", False),
        port=app_config.get("PORT", 5000),
        host=app_config.get("HOST", "localhost")
    )

if __name__ == "__main__":
    #old_main()
    new_main()
