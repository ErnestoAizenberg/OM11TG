from typing import Dict, Tuple, Optional
import logging
import requests

from app.config_manager import UserConfigManager
from app.logs import logger
from app.messages import MessageBuilder

BOT_API_URL = "https://api.telegram.org/bot"


class TelegramManager:
    def __init__(
        self,
        logger: logging.Logger,
        config_manager: UserConfigManager,
        message_creator: MessageBuilder,
        server_address: str,
    ):
        self.logger = logger
        self.config_manager = config_manager
        self.message_creator = message_creator
        self.server_address = server_address

    def test_connection(self, bot_token: str, chat_id: str) -> Tuple[bool, str]:
        logger.info("Starting Telegram API connection test.")
        try:
            me_response = requests.get(
                f"https://api.telegram.org/bot{bot_token}/getMe", timeout=10
            )
            logger.debug("Response from getMe: %s", me_response.json())

            if not me_response.json().get("ok"):
                logger.error("Invalid bot token: %s", bot_token)
                return False, "Неверный токен бота"

            message_text = self.message_creator.telegram_connected(self.server_address)
            logger.debug("Message text created: %s", message_text)

            send_response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"},
                timeout=10,
            )
            logger.debug("Response from sendMessage: %s", send_response.json())

            if not send_response.json().get("ok"):
                logger.error("Failed to send message. Chat ID: %s", chat_id)
                return False, "Не удалось отправить сообщение (проверьте Chat ID)"

            logger.info(
                "Successfully connected to Telegram. Message sent to Chat ID: %s",
                chat_id,
            )
            return True, "Успешно подключено"

        except requests.exceptions.RequestException as e:
            logger.error("Failed to connect to Telegram API: %s", str(e))
            return False, f"Ошибка соединения: {str(e)}"

    def send_message(
        self,
        user_id: str,
        message_text: str,
        parse_mode: Optional[str] = None,
    ) -> Tuple[Dict, int]:
        logger.info("Attempting to send message for user %s", user_id)

        if not message_text:
            logger.warning("Message content is required.")
            return {
                "success": False,
                "error": "Сообщение обязательно для заполнения",
            }, 400

        config = self.config_manager.load_config(user_id)
        if not config:
            logger.warning("No Telegram config found for user %s", user_id)
            return {"success": False, "error": "Телеграм бот не подключен"}, 400

        bot_token = config.get("bot_token")
        chat_id = config.get("chat_id")

        if not bot_token or not chat_id:
            logger.error("Incomplete Telegram config for user %s", user_id)
            return {"success": False, "error": "Неполная конфигурация Telegram"}, 400

        try:
            payload = {"chat_id": chat_id, "text": message_text}
            if parse_mode:
                payload["parse_mode"] = parse_mode

            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json=payload,
                timeout=10,
            )
            response_data = response.json()

            if not response_data.get("ok"):
                error_msg = response_data.get(
                    "description", "Не удалось отправить сообщение"
                )
                logger.error("Telegram API error for user %s: %s", user_id, error_msg)
                return {"success": False, "error": error_msg}, 400

            logger.info("Message successfully sent to user %s", user_id)
            return {
                "success": True,
                "message": "Сообщение успешно отправлено",
                "message_id": response_data.get("result", {}).get("message_id"),
            }, 200

        except requests.exceptions.RequestException as e:
            logger.error("Error sending message for user %s: %s", user_id, str(e))
            return {"success": False, "error": str(e)}, 500
        except Exception as e:
            logger.error(
                "Unexpected error sending message for user %s: %s", user_id, str(e)
            )
            return {
                "success": False,
                "error": "Внутренняя ошибка сервера",
            }, 500

    def check_webhook(self, token):
        self.logger.debug("Checking webhook for token: %s", token)
        response = requests.get(f"https://api.telegram.org/bot{token}/getWebhookInfo")
        self.logger.debug("getWebhookInfo response status: %s", response.status_code)

        if response.ok:
            data = response.json()
            self.logger.debug("Webhook info retrieved: %s", data)
            if data["result"]["url"]:  # Если есть URL, то вебхук установлен
                self.logger.info("Webhook is already set for token: %s", token)
                return True
            else:
                self.logger.info("No webhook set for token: %s", token)
        else:
            self.logger.error(
                "Failed to get webhook info for token %s, status code: %s",
                token,
                response.status_code,
            )

        return False

    def set_webhook(self, token):
        url = f"{self.server_address}/webhook/{token}"
        self.logger.info("Setting webhook for token: %s with URL: %s", token, url)

        response = requests.get(f"{BOT_API_URL}{token}/setWebhook?url={url}")
        self.logger.info("setWebhook response status: %s", response.status_code)

        if response.ok:
            self.logger.info("Webhook successfully set for token: %s", token)
        else:
            self.logger.error(
                "Failed to set webhook for token: %s, status code: %s",
                token,
                response.status_code,
            )

        return response.ok

    def set_webhooks(self):
        bot_tokens = self.config_manager.get_bot_tokens()
        self.logger.info("Setting webhooks for tokens...")

        for token in bot_tokens:
            if self.check_webhook(token):
                if self.set_webhook(token):
                    self.logger.info("Webhook установлен для токена: %s", token)
                else:
                    self.logger.error("Ошибка установки вебхука для токена: %s", token)
            else:
                self.logger.warning("Token is invalid or already registered: %s", token)
