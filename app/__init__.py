from flask import Flask

from app.api import configure_api
from app.config_manager import UserConfigManager
from app.extensions import init_redis
from app.logs import logger
from app.messages import MessageBuilder, MessageTemplates
from app.session_manager import TelegramSessionManager
from app.updates import CommandHandler
from config import RedisConfig

from app.manus_api import ManusAgent

# from app.manager import TelegramManager

__all__ = ["create_app"]
TG_CONFIGS_DIR = "instance/user_configs"
BOT_API_URL = "https://api.telegram.org/bot"
# SERVER_ADDRESS = app.config.get("SERVER_ADDRESS")
MANUS_AGENT_ADDRES = "http://localhost:5001/api"


def create_app(app_config, redis_config: RedisConfig):
    app = Flask(__name__)
    app.state_config = app_config

    manus_agent = ManusAgent(
        agent_url=MANUS_AGENT_ADDRES,
        logger=logger,
    )
    redis_client = init_redis(redis_config)
    templates = MessageTemplates()
    message_builder = MessageBuilder(templates)

    session_manager = TelegramSessionManager(redis_client)
    config_manager = UserConfigManager(config_dir=TG_CONFIGS_DIR)
    # telegram_manager = TelegramManager(
    #    config_manager=config_manager,
    #    message_creator=message_builder,
    #    server_address=SERVER_ADDRESS,
    # )
    command_handler = CommandHandler(
        logger=logger,
        manus_agent=manus_agent,
        config_manager=config_manager,
        message_builder=message_builder,
        session_manager=session_manager,
        bot_api_url=BOT_API_URL,
    )
    configure_api(
        app=app,
        logger=logger,
        command_handler=command_handler,
    )
    return app
