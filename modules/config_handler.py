import json
from pathlib import Path


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

    def __init__(self):
        self.config_path = Path("config.json")
        self._isConfigExists()
        self.config = self.load_config()

    def load_config(self):
        try:
            with self.config_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка чтения конфига\n{e}")

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
                print("Файл конфигурации успешно создан")
            except Exception as e:
                print(f"Не удалось создать файл конфигурации\n{e}")
