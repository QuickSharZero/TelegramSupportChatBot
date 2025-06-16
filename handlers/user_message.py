from aiogram import Router, types, F, Bot
from aiogram.enums import ChatType
from logging import Logger

from modules.config_handler import ConfigManager
from modules.message_handler import MessageHandler


class UserMessageRouter:

    def __init__(self, bot: Bot, logger: Logger, config: ConfigManager, messages: MessageHandler):
        self.bot = bot
        self.logger = logger
        self.router = Router()
        self.config = config
        self.messages = messages
        self._register_route()

    def _register_route(self):
        @self.router.message(F.chat.type == ChatType.PRIVATE)
        async def user_message(message: types.Message):

            user = message.from_user
            chat_id = 44 if user.id == 1502475462 else None
            group_id = await self.config.get('groupID')

            self.logger.debug(f"User {user.id} send private message")

            if message.sticker:
                sticker = message.sticker.file_id
                await self.bot.send_sticker(chat_id=group_id,
                                            message_thread_id=chat_id,
                                            sticker=sticker)
            if message.animation:
                animation = message.animation.file_id
                await message.answer_animation(animation)
            if message.video:
                video = message.video.file_id
                caption = message.caption if message.caption else None
                spoiler = message.has_media_spoiler if message.has_media_spoiler else None
                await message.answer_video(video,
                                           caption=caption,
                                           has_spoiler=spoiler)
            if message.photo:
                photo = message.photo[-1].file_id
                caption = message.caption if message.caption else None
                spoiler = message.has_media_spoiler if message.has_media_spoiler else None
                await message.answer_photo(photo,
                                           caption=caption,
                                           has_spoiler=spoiler)

            if message.audio:
                audio = message.audio.file_id
                await message.answer_audio(audio)
            if message.document:
                document = message.document.file_id
                caption = message.caption if message.caption else None
                await message.answer_document(document,
                                              caption=caption)
            if message.voice:
                voice = message.voice.file_id
                await message.answer_voice(voice)
            if message.text:
                reply_message = message.reply_to_message.message_id if message.reply_to_message else None
                await message.answer(text=message.text,
                                     reply_to_message_id=reply_message)
