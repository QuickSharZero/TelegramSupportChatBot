from aiogram import Router, types
from aiogram.filters import Command

from modules.message_handler import MessageHandler
from modules.config_handler import ConfigManager


class GetChatInfoRouter:

    def __init__(self, config: ConfigManager, messages: MessageHandler):
        self.router = Router()
        self.config = config
        self.messages = messages
        self._register_router()

    def _register_router(self):
        @self.router.message(Command('get_chat_info'))
        async def get_chat_info_command(message: types.Message):
            user = message.from_user
            admins = await self.config.get('admins')

            if user.id in admins:
                text = await self.messages.get(key="get_chat_info", message=message)
                await message.answer(text=text, parse_mode="Markdown")
                return

            text = await self.messages.get(key="errors.NoPerm")
            await message.answer(text=text, parse_mode="Markdown")
