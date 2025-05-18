import yaml
from pathlib import Path


class MessageHandler:

    default_messages = {
        "start": {
            "greeting": "Привет! \nНапиши мне сообщения и я отправлю его техподдержке."
        },
        "reload_messages": {
            "succes": "Сообщения бота успешно перезагружены"
        }
    }

    def __init__(self):
        self.messages_file = Path("messages.yml")
        self._isFileExists()

        self.messages = self.load_messages()

    def load_messages(self) -> dict:
        try:
            with self.messages_file.open('r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Ошибка чтения списка сообщений\n{e}")

    async def reload(self):
        self.messages = self.load_messages()

    async def get(self, *keys):
        value = self.messages
        for key in keys:
            value = value.get(key, {})
        return value

    def _isFileExists(self):
        try:
            if not self.messages_file.exists():
                with self.messages_file.open('w', encoding='utf-8') as f:
                    yaml.dump(self.default_messages, f)
                    print("Файл сообщений создан!")
        except Exception as e:
            print(f"Не удалось создать файл сообшений\n{e}")
