from flask import jsonify, request


def configure_api(app, logger, command_handler):
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
                raise ValueError("Unformated request")
        except Exception as e:
            logger.exception("Unexpected error occurred while handling update: %s", e)
            return jsonify({"status": "error"}), 500
