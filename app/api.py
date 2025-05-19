import logging
from flask import jsonify, request
from app.manager import TelegramManager
from typing import Callable, Tuple, Dict

configs = {}


def configure_api(
    app,
    logger: logging.Logger,
    command_handler,
    telegram_manager: TelegramManager,
    generate_uuid_32: Callable,
):
    @app.route("/webhook/<token>", methods=["POST"])
    def webhook(token):
        try:
            update = request.json
            logger.info("Update received: %s", update)

            if update and update.get("message"):
                text = update["message"].get("text", "")
                if text.startswith("/start"):
                    command_handler.handle_start(update, token)
                elif text.startswith("/auth"):
                    command_handler.handle_auth(update, token)
                else:
                    logger.info("Handling message from bot: %s", token)
                    command_handler.handle_message(update, token)

                return jsonify({"status": "ok"}), 200
            else:
                raise ValueError("Unformatted request")
        except Exception as e:
            logger.exception("Unexpected error occurred while handling update: %s", e)
            return jsonify({"status": "error"}), 500

    @app.route("/api/telegram/set_webhook", methods=["POST"])
    def setup_webhook():
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400

        user_id = data.get("user_id", "default")
        bot_token = data.get("bot_token")
        chat_id = data.get("chat_id")

        try:
            # Test connection
            success = telegram_manager.test_connection(bot_token, chat_id)
            if not success:
                return (
                    jsonify(
                        {"success": False, "error": "Failed to connect to Telegram API"}
                    ),
                    400,
                )

            # Save config
            config = {"bot_token": bot_token, "chat_id": chat_id, "user_id": user_id}
            configs[user_id] = config

            # Set webhook
            set_webhook_success = telegram_manager.set_webhook(bot_token)
            if not set_webhook_success:
                return (
                    jsonify({"success": False, "error": "Failed to set webhook"}),
                    500,
                )

            return jsonify({"success": True, "message": "Webhook set successfully"})
        except Exception as e:
            app.logger.exception("Error in setup_webhook")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/telegram/send_message", methods=["POST"])
    def send_message():
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400

        user_id = data.get("user_id")
        message_text = data.get("message_text")

        if not user_id or not message_text:
            return jsonify({"success": False, "error": "Invalid data received"}), 400

        try:
            resp: Tuple = telegram_manager.send_message(
                user_id=user_id,
                message_text=message_text,
                parse_mode=None,
            )
            status: Dict = resp[0]
            status_code: int = resp[1]

            if not status.get("succcess"):
                error_message = status.get("error", "Unknown Error")
                reponse_message = f"Failed to send message: {error_message}"
                return (
                    jsonify({"success": False, "error": reponse_message}),
                    500,
                )

            return jsonify({"success": True, "message": "Message sent"})
        except Exception as e:
            app.logger.exception("Error in send_message")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/api/telegram/disconnect", methods=["POST"])
    def disconnect():
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400

        user_id = data.get("user_id")
        if user_id in configs:
            del configs[user_id]
            return jsonify({"success": True, "message": "Disconnected successfully"})
        else:
            return jsonify({"success": False, "error": "No configuration found"}), 404

    @app.route("/api/telegram/status", methods=["GET"])
    def status():
        user_id = request.args.get("user_id")
        is_connected = user_id in configs
        return jsonify(
            {
                "success": True,
                "status": "connected" if is_connected else "disconnected",
                "user_id": user_id,
            }
        )
