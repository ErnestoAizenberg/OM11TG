import requests
from typing import List


class CommandHandler:
    def __init__(
        self,
        logger,
        manus_agent,
        config_manager,
        message_builder,
        session_manager,
        bot_api_url: str,
    ):
        self.logger = logger
        self.manus_agent = manus_agent
        self.config_manager = config_manager
        self.message_builder = message_builder
        self.session_manager = session_manager
        self.bot_api_url = bot_api_url

    def _send_message(self, bot_token: str, chat_id, text: str):
        url = f"{self.bot_api_url}{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)

    def handle_message(self, update, bot_token):
        message = update["message"].get("text")
        user = update["message"].get("from")
        tg_id = user.get("id")
        self.logger.info(f"tg_id: {tg_id}")

        user_info = self.session_manager.get_user(tg_id)
        self.logger.info(f"user_info: {user_info}")

        if user_info:
            user_uuid = user_info.get("user_uuid")
            if user_uuid:
                try:
                    output_chain: List[str] = self.manus_agent.execute_command(
                        message, user_uuid
                    )
                    for chain in output_chain:
                        self._send_message(bot_token, user["id"], chain)
                except Exception as e:
                    self.logger(f"An error: {str(e)}")
                    error_message = (
                        "ОШИБКА: произошла неожижаная ошибка при обращении к агенту"
                    )
                    self._send_message(
                        bot_token,
                        user["id"],
                        error_message,
                    )

        # Если пользователь не авторизован
        template = self.message_builder.auth_required()
        self._send_message(bot_token, user["id"], template)

    def handle_start(self, update, bot_token):
        if not update.get("message"):
            return

        user = update["message"]["from"]
        # Можно добавить дополнительные проверки или логирование
        welcome_template = self.message_builder.start(first_name=user["first_name"])
        self._send_message(bot_token, user["id"], welcome_template)

    def handle_auth(self, update, bot_token):
        if not update.get("message"):
            return

        user = update["message"]["from"]
        text = update["message"].get("text", "")
        command_parts = text.split()

        if len(command_parts) < 2:
            self._send_message(
                bot_token,
                user["id"],
                f"Validation error, {user['first_name']}, please provide web token",
            )
            return

        auth_token = command_parts[1]
        first_name = user["first_name"]
        web_user_uuid = self.config_manager.user_uuid_by_authtoken(auth_token)

        if web_user_uuid:
            self.session_manager.add_user(
                tg_id=user["id"],
                user_uuid=web_user_uuid,
            )
            auth_success_template = self.message_builder.welcome(first_name)
            self._send_message(bot_token, user["id"], auth_success_template)
        else:
            auth_invalid_template = self.message_builder.auth_invalid()
            self._send_message(bot_token, user["id"], auth_invalid_template)
