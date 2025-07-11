import yaml
from pathlib import Path
from aiogram.types import Message
import re
from typing import Optional
from logging import Logger


class MessageHandler:

    default_messages = {
        # Сообщения поддерживают форматирование Markdown и плейсхолдеры:
        # {username}, {user_id}, {user_first_name}, {user_last_name},
        # {chat_id}, {chat_is_forum}, {thread_id}
        "start": {
            "greeting": "Привет! \nНапиши мне сообщения и я отправлю его техподдержке."
        },
        "reload_messages": {
            "succes": "Сообщения бота успешно перезагружены",
            "reload": "Не удалось обновить сообщения бота"
        },

        "get_chat_info": "ID чата: `{chat_id}`\nЭто форум?: {chat_is_forum}\nThread ID: `{thread_id}`",

        "errors": {
            "NoPerm": "Вы не можете использовать данную команду"
        }
    }

    def __init__(self, logger: Logger):
        self.messages_file = Path("messages.yml")
        self.logger = logger

        self._isFileExists()

        self.messages = self.load_messages()

    def load_messages(self) -> dict:
        try:
            with self.messages_file.open('r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Ошибка чтения списка сообщений: {e}", exc_info=True)

    async def reload(self):
        self.messages = self.load_messages()

    async def get(self, key: str, message: Optional[Message] = None):
        messages = self.messages
        keys = key.split('.')
        for k in keys:
            messages = messages.get(k, {})

        context = {}
        if message:
            context.update({
                'username': message.from_user.username,
                'user_id': message.from_user.id,
                'user_first_name': message.from_user.first_name,
                'user_last_name': message.from_user.last_name,
                'chat_id': message.chat.id,
                'chat_is_forum': message.chat.is_forum,
                'thread_id': message.message_thread_id
            })

        return messages.format(**context)

    def _isFileExists(self):
        try:
            if not self.messages_file.exists():
                with self.messages_file.open('w', encoding='utf-8') as f:
                    yaml.dump(self.default_messages, f)
                self.logger.info("Файл сообщений создан!")
        except Exception as e:
            self.logger.error(f"Не удалось создать файл сообщений\n{e}", exc_info=True)
