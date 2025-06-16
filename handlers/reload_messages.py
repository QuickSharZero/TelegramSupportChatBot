from aiogram import Router, types
from aiogram.filters import Command
from logging import Logger

from modules.message_handler import MessageHandler
from modules.config_handler import ConfigManager


class ReloadMessageRouter:

    def __init__(self, logger: Logger, config: ConfigManager, messages: MessageHandler):
        self.router = Router()
        self.logger = logger
        self.messages = messages
        self.config = config
        self._register_router()

    def _register_router(self):
        @self.router.message(Command('reload_messages'))
        async def reload_messages_command(message: types.Message):

            admins = await self.config.get('admins')

            if message.from_user.id in admins:
                try:
                    await self.messages.reload()
                    text = await self.messages.get(key="reload_messages.success", message=message)
                    await message.answer(text, parse_mode="Markdown")
                    return
                except Exception as e:
                    text = await self.messages.get(key="reload_messages.error", message=message)
                    await message.answer(text, parse_mode="Markdown")
                    print(f"Ошибка перезагрузки сообщений\n{e}")
                    return

            text = await self.messages.get(key="errors.NoPerm", message=message)
            await message.answer(text, parse_mode="Markdown")

