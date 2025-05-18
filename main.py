import aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from modules.config_handler import ConfigManager
from modules.message_handler import MessageHandler

from handlers.start import StartRouter
from handlers.reload_messages import ReloadMessageRouter
from handlers.get_chat_info import GetChatInfoRouter


class TelegramBot:

    def __init__(self):
        self.config = ConfigManager()
        self.messages = MessageHandler()

        TOKEN = asyncio.run(self.config.get("token"))

        self.bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()

    async def run(self):
        print("Bot starting...")
        try:
            start = StartRouter(messages=self.messages)
            reload_messages = ReloadMessageRouter(config=self.config, messages=self.messages)
            get_chat_info = GetChatInfoRouter(config=self.config, messages=self.messages)

            self.dp.include_router(start.router)
            self.dp.include_router(reload_messages.router)
            self.dp.include_router(get_chat_info.router)

            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot)
        except Exception as e:
            print(f"Bot stopped with error:\n{e}")
        finally:
            print("Bot has been stopped")


if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.run())
