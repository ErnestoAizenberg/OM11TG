from dataclasses import dataclass
from typing import Optional

AUTH_TOKEN_LENGTH = 32
AUTH_TIMEOUT = 300


@dataclass
class MessageTemplates:

    START: str = (
        "Добро пожаловать, {first_name}!\n\n"
        "om11 ваш проффесиональный AI помощник\n\n"
        "Для доступа к функциям бота отправьте команду:\n"
        "👉 /auth <ваш_токен>\n\n"
    )

    WELCOME: str = (
        "🌟 Добро пожаловать, {full_name}!\n" "✅ Вы успешно аутентифицированы."
    )

    AUTH_REQUIRED: str = (
        "🔒 Требуется аутентификация\n\n"
        "Для доступа к функциям бота отправьте команду:\n"
        "👉 /auth <ваш_токен>\n\n"
        f"🔑 Токен должен содержать {AUTH_TOKEN_LENGTH} символов."
    )

    TELEGRAM_CONNECTED: str = (
        "🤖 Бот успешно подключен!\n\n"
        "Теперь все логи и уведомления будут приходить сюда.\n"
        '<a href="{server_address}">⚙️ Управление подключением</a>'
    )

    AUTH_EXPIRED: str = (
        "⏳ Срок действия токена истек\n" "Пожалуйста, запросите новый токен."
    )

    AUTH_INVALID: str = (
        "❌ Неверный токен\n" "Проверьте правильность ввода и попробуйте снова."
    )

    HELP: str = (
        "🛠 Доступные команды:\n\n"
        "/auth - начать аутентификацию\n"
        "/help - показать справку"
    )


class MessageBuilder:
    def __init__(self, templates: Optional[MessageTemplates] = None):
        self.templates = templates or MessageTemplates()

    def welcome(self, full_name: str) -> str:
        return self.templates.WELCOME.format(full_name=full_name)

    def auth_required(self) -> str:
        return self.templates.AUTH_REQUIRED

    def telegram_connected(self, server_address: str) -> str:
        return self.templates.TELEGRAM_CONNECTED.format(server_address=server_address)

    def auth_expired(self) -> str:
        return self.templates.AUTH_EXPIRED

    def auth_invalid(self) -> str:
        return self.templates.AUTH_INVALID

    def help(self) -> str:
        return self.templates.HELP

    def start(self, first_name: str) -> str:
        return self.templates.START.format(first_name=first_name)
