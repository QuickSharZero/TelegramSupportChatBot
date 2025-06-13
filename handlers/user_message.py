from aiogram import Router, types

from modules.config_handler import ConfigManager
from modules.message_handler import MessageHandler


class UserMessageRouter:

    def __init__(self, config: ConfigManager, messages: MessageHandler):
        self.router = Router()
        self.config = config
        self.messages = messages
        self._register_route()

    def _register_route(self):
        @self.router.message()
        async def user_message(message: types.Message):
            if not message.chat.type == 'private':
                return
            user = message.from_user
            if message.sticker:
                sticker = message.sticker.file_id
                await message.answer_sticker(sticker)
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
            if message.text:
                await message.answer(text=message.text)
