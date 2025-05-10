import json
import os
from typing import Dict, Optional

from app.logs import logger


def read_json_file(file_path):
    """Читает JSON-файл и возвращает его содержимое или None в случае ошибки."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"❌ Некорректный JSON в файле: {file_path}")
        return None


def find_first_json_file_with_string(directory, search_string):
    print("🔍 Начинаем поиск в директории:", directory)
    print("🔍 Ищем строку:", search_string)

    # Проходим по всем файлам в указанной директории
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            print(f"📄 Проверяем файл: {filename}")

            data = read_json_file(file_path)
            if data is None:
                continue  # Пропустить, если не удалось прочитать файл

            # Проверяем наличие строки в данных
            if isinstance(data, dict):
                if any(search_string in str(value) for value in data.values()):
                    print(f"✅ Найдено совпадение в файле: {filename}")
                    return os.path.splitext(filename)[
                        0
                    ]  # Возвращаем имя файла без расширения

            elif isinstance(data, list):
                if any(search_string in str(item) for item in data):
                    print(f"✅ Найдено совпадение в файле: {filename}")
                    return os.path.splitext(filename)[
                        0
                    ]  # Возвращаем имя файла без расширения

    print("🔍 Поиск завершен. Совпадений не найдено.")
    return None  # Если не найдено совпадений


def get_json_file_names(directory):
    """Возвращает спискок имён всех .json файлов в директории без расширения."""
    json_file_names = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            json_file_names.append(
                os.path.splitext(filename)[0]
            )  # Добавляем имя без расширения

    return json_file_names


class UserConfigManager:
    def __init__(self, config_dir: str = "instance/user_configs"):
        self.config_dir = config_dir
        os.makedirs(self.config_dir, exist_ok=True)

    def get_user_config_path(self, user_id: str) -> str:
        return os.path.join(self.config_dir, f"{user_id}.json")

    def save_config(self, user_id: str, config: Dict) -> bool:
        try:
            with open(self.get_user_config_path(user_id), "w") as f:
                json.dump(config, f, separators=(",", ":"))
            logger.info(f"Telegram config saved for user {user_id}")
            return True
        except (IOError, PermissionError) as e:
            logger.error(f"Failed to save Telegram config for user {user_id}: {e}")
            return False

    def load_config(self, user_id: str) -> Optional[Dict]:
        config_path = self.get_user_config_path(user_id)
        if not os.path.exists(config_path):
            logger.warning(f"No config file found for user {user_id}")
            return None

        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Error reading config for user {user_id}: {e}")
            return None

    def delete_config(self, user_id: str) -> bool:
        try:
            os.remove(self.get_user_config_path(user_id))
            logger.info(f"Telegram disconnected for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing config for user {user_id}: {e}")
            return False

    def get_json_file_names(self, directory):
        """Возвращает спискок имён всех .json файлов в директории без расширения."""
        json_file_names = []

        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                json_file_names.append(
                    os.path.splitext(filename)[0]
                )  # Добавляем имя без расширения

        return json_file_names

    def check_user_config(self, user_uuid):
        result = user_uuid in self.get_json_file_names(self.config_dir)
        return result

    def find_user_config_for_bot(self, bot_token):
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.config_dir, filename)) as f:
                    if bot_token in f.read():
                        return filename
        return None

    def get_uuid_by_bot_token(self, bot_token):
        filename = self.find_user_config_for_bot(bot_token)
        if filename:
            user_id = os.path.splitext(filename)[0]
            return user_id
        return None

    def user_uuid_by_authtoken(self, authtoken):
        return self.get_uuid_by_bot_token(authtoken)

    def get_bot_tokens(self):
        bot_tokens = []

        # Проходим по всем файлам в указанной директории
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.config_dir, filename)
                data = read_json_file(file_path)

                if data and "bot_token" in data:
                    bot_tokens.append(data["bot_token"])

        return bot_tokens

    def get_auth_tokens(self):
        auth_tokens = []

        # Проходим по всем файлам в указанной директории
        for filename in os.listdir(self.config_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(self.config_dir, filename)
                data = read_json_file(file_path)

                if data and "auth_token" in data:
                    auth_tokens.append(data["auth_token"])

        return auth_tokens
