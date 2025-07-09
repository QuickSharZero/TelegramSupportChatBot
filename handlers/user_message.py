from aiogram import Router, types, F, Bot
from aiogram.enums import ChatType
from logging import Logger

from modules.config_handler import ConfigManager
from modules.message_handler import MessageHandler
from modules.database_handler import DatabaseHandler


class UserMessageRouter:

    def __init__(self, bot: Bot, logger: Logger, database: DatabaseHandler, config: ConfigManager, messages: MessageHandler):
        self.bot = bot
        self.logger = logger
        self.database = database
        self.router = Router()
        self.config = config
        self.messages = messages
        self._register_route()

    def _register_route(self):
        @self.router.message(F.chat.type == ChatType.PRIVATE)
        async def user_message(message: types.Message):

            user = message.from_user
            thread_id = await self.database.getThreadID(tgID=user.id)  # ID форума
            chat_id = await self.config.get('groupID')  # ID группы

            if await self.database.isUserBlocked(tgID=user.id):
                return

            if message.media_group_id:
                await self.bot.send_media_group(chat_id=chat_id,
                                                message_thread_id=thread_id,
                                                media=message.media_group_id)

            if message.sticker:
                sticker = message.sticker.file_id
                await self.bot.send_sticker(chat_id=chat_id,
                                            message_thread_id=thread_id,
                                            sticker=sticker)
            if message.animation:
                animation = message.animation.file_id
                await self.bot.send_animation(chat_id=chat_id,
                                              message_thread_id=thread_id,
                                              animation=animation)
            if message.video:
                video = message.video.file_id
                caption = message.caption if message.caption else None
                spoiler = message.has_media_spoiler if message.has_media_spoiler else None
                await self.bot.send_video(chat_id=chat_id,
                                          message_thread_id=thread_id,
                                          video=video,
                                          caption=caption,
                                          has_spoiler=spoiler)
            if message.photo:
                photo = message.photo[-1].file_id
                caption = message.caption if message.caption else None
                spoiler = message.has_media_spoiler if message.has_media_spoiler else None
                await self.bot.send_photo(chat_id=chat_id,
                                          message_thread_id=thread_id,
                                          photo=photo,
                                          caption=caption,
                                          has_spoiler=spoiler)

            if message.audio:
                audio = message.audio.file_id
                await self.bot.send_audio(chat_id=chat_id,
                                          message_thread_id=thread_id,
                                          audio=audio)
            if message.document:
                document = message.document.file_id
                caption = message.caption if message.caption else None
                await self.bot.send_document(chat_id=chat_id,
                                             message_thread_id=thread_id,
                                             document=document,
                                             caption=caption)
            if message.voice:
                voice = message.voice.file_id
                await self.bot.send_voice(chat_id=chat_id,
                                          message_thread_id=thread_id,
                                          voice=voice)
            if message.text:
                reply_message = message.reply_to_message.message_id if message.reply_to_message else None
                await self.bot.send_message(chat_id=chat_id,
                                            message_thread_id=thread_id,
                                            text=message.text,
                                            reply_to_message_id=reply_message)
