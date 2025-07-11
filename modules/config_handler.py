import json
from pathlib import Path
from logging import Logger


class ConfigManager:

    default_config = {
        "token": "",
        "groupID": "",
        "admins": [
            0
        ],
        "postgres": {
            "host": "host",
            "port": 5432,
            "username": "username",
            "password": "password",
            "database": "database"
        }
    }

    def __init__(self, logger: Logger):
        self.config_path = Path("config.json")
        self.logger = logger

        self._isConfigExists()
        self.config = self.load_config()

    def load_config(self):
        try:
            with self.config_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Ошибка чтения конфига: {e}", exc_info=True)

    async def get(self, *keys):
        value = self.config
        for key in keys:
            value = value.get(key, {})
        return value

    async def reload(self):
        self.config = self.load_config()

    def _isConfigExists(self):
        if not self.config_path.exists():
            try:
                with self.config_path.open('w', encoding='utf-8') as f:
                    json.dump(self.default_config, f, indent=4)
                self.logger.info("Файл конфигурации успешно создан")
            except Exception as e:
                self.logger.error(f"Не удалось создать файл конфигурации: {e}", exc_info=True)
