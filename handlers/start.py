from aiogram import Router, types
from aiogram.filters import Command

from modules.message_handler import MessageHandler


class StartRouter:

    def __init__(self, messages: MessageHandler):
        self.router = Router()
        self.messages = messages
        self._register_router()

    def _register_router(self):
        @self.router.message(Command('start'))
        async def start_command(message: types.Message):
            text = await self.messages.get(key="start.greeting", message=message)
            await message.answer(text, parse_mode='Markdown')

