# config.py

import os
import argparse
from dotenv import load_dotenv

# Load environment variables from the specified .env file
load_dotenv("instance/.env")


def parse_arguments():
    """
    Parse command-line arguments for configuration overrides.
    """
    parser = argparse.ArgumentParser(description="Flask app with Redis support.")

    parser.add_argument("--server_address", type=str, help="URL of the server.")
    parser.add_argument("--secret_key", type=str, help="Secret key for Flask app.")
    parser.add_argument("--redis_host", type=str, help="Redis server host.")
    parser.add_argument("--redis_port", type=int, help="Redis server port.")
    parser.add_argument("--redis_db", type=int, help="Redis database number.")
    parser.add_argument("--host", type=str, help="Server host.")
    parser.add_argument("--port", type=int, help="Server port.")

    return parser.parse_args()


# Parse command-line arguments
args = parse_arguments()


def get_input(prompt, default=None):
    """
    Prompt the user for input, with an optional default.
    """
    user_input = input(f"{prompt} (default: {default}): ")
    return user_input if user_input else default


class APIURLConfig:
    """
    Class holding API URL configurations.
    """

    OM11: str = "https://c081-34-91-46-134.ngrok-free.app"
    OM11TG: str = "http://localhost:5001"

    def get(self, key, default=None):
        return getattr(self, key, default)


class DefConfig:
    """
    Placeholder for default configurations.
    """

    pass


class Config:
    """
    Basic Flask configuration class.
    """

    SECRET_KEY = args.secret_key or get_input("Enter secret key", "llmlllmlllmlm")
    DEBUG = os.getenv("FLASK_DEBUG", "true").lower() in ["true", "1", "t"]
    SERVER_ADDRESS = args.server_address or get_input(
        "Server address", "https://example.com"
    )
    HOST = args.host or get_input("Host", "localhost")
    PORT = args.port or int(get_input("Port", "5001"))

    def get(self, key, default=None):
        return getattr(self, key, default)


class RedisConfig:
    """
    Redis configuration settings.
    """

    HOST = args.redis_host or get_input("Redis host", "localhost")
    PORT = args.redis_port or int(get_input("Redis port", "6379"))
    DB = args.redis_db or int(get_input("Redis database number", "0"))
    DECODE_RESPONSES = True

    def get(self, key, default=None):
        return getattr(self, key, default)
