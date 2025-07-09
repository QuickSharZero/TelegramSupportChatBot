from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.enums import ParseMode
from logging import Logger

from modules.message_handler import MessageHandler
from modules.config_handler import ConfigManager
from modules.database_handler import DatabaseHandler


class StartRouter:

    def __init__(self, bot: Bot, logger: Logger, database: DatabaseHandler, config: ConfigManager, messages: MessageHandler):
        self.bot = bot
        self.logger = logger
        self.database = database
        self.router = Router()
        self.config = config
        self.messages = messages
        self._register_router()

    def _register_router(self):
        @self.router.message(Command('start'))
        async def start_command(message: types.Message):
            user = message.from_user
            if user.is_bot:
                return

            if not await self.database.checkUserExists(tgID=user.id):

                thread = await self.bot.create_forum_topic(chat_id=int(await self.config.get("groupID")),
                                                           name=message.from_user.username)

                threadID = thread.message_thread_id  # id созданного чата

                await self.database.addUser(tgID=user.id,
                                            username=user.username,
                                            threadID=threadID)

            text = await self.messages.get(key="start.greeting", message=message)
            await message.answer(text, parse_mode=ParseMode.MARKDOWN)

