from aiogram import Router, types
from aiogram.filters import Command

from modules.message_handler import MessageHandler
from modules.config_handler import ConfigManager

class ReloadMessageRouter:

    def __init__(self, config: ConfigManager, messages: MessageHandler):
        self.router = Router()
        self.messages = messages
        self.config = config
        self._register_router()

    def _register_router(self):
        @self.router.message(Command('reload_messages'))
        async def reload_messages_command(message: types.Message):
            text = await self.messages.get('start', 'greeting')
            await message.answer(text)

