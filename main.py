import aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio
import logging

from modules.config_handler import ConfigManager
from modules.message_handler import MessageHandler
from modules.database_handler import DatabaseHandler

from handlers.start import StartRouter
from handlers.reload_messages import ReloadMessageRouter
from handlers.get_chat_info import GetChatInfoRouter
from handlers.user_message import UserMessageRouter
from handlers.admins_message import AdminsMessageRouter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class TelegramBot:

    def __init__(self):
        self.logger = logger
        self.config = ConfigManager(logger=self.logger)
        self.messages = MessageHandler(logger=self.logger)
        self.database = DatabaseHandler(logger=self.logger, config=self.config)

        if asyncio.run(self.database.check_connection()):
            self.logger.info("База данных успешно подключена")
            asyncio.run(self.database.create_tables())

        TOKEN = asyncio.run(self.config.get("token"))

        self.bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()

    async def run(self):
        self.logger.info("Bot starting...")
        try:
            start = StartRouter(bot=self.bot, logger=self.logger, database=self.database, config=self.config, messages=self.messages)
            reload_messages = ReloadMessageRouter(logger=self.logger, config=self.config, messages=self.messages)
            get_chat_info = GetChatInfoRouter(logger=self.logger, config=self.config, messages=self.messages)
            user_message = UserMessageRouter(bot=self.bot, logger=self.logger, database=self.database, config=self.config, messages=self.messages)
            admins_message = AdminsMessageRouter(bot=self.bot, logger=self.logger, database=self.database, config=self.config, messages=self.messages)

            self.dp.include_router(start.router)
            self.dp.include_router(reload_messages.router)
            self.dp.include_router(get_chat_info.router)
            self.dp.include_router(user_message.router)
            self.dp.include_router(admins_message.router)

            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except Exception:
            self.logger.error(f"Bot stopped with error", exc_info=True)
        finally:
            self.logger.info("Bot has been stopped")


if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.run())
