from aiogram import Router, types, F, Bot
from aiogram.enums import ChatType
from aiogram.types import ReactionTypeEmoji
from logging import Logger

from modules.config_handler import ConfigManager
from modules.message_handler import MessageHandler


class AdminsMessageRouter:

    def __init__(self, bot: Bot, logger: Logger, config: ConfigManager, messages: MessageHandler):
        self.bot = bot
        self.logger = logger
        self.router = Router()
        self.config = config
        self.messages = messages
        self._register_route()

    def _register_route(self):
        @self.router.message(F.chat.type == ChatType.SUPERGROUP)
        async def user_message(message: types.Message):

            user = message.from_user
            reaction = [ReactionTypeEmoji(emoji="👍")]

            chat_id = 1502475462 if message.message_thread_id == 44 else message.chat.id

            if message.sticker:
                sticker = message.sticker.file_id
                await self.bot.send_sticker(chat_id=chat_id,
                                            sticker=sticker)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            if message.animation:
                animation = message.animation.file_id
                await self.bot.send_animation(chat_id=chat_id,
                                              animation=animation)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            elif message.video:
                video = message.video.file_id
                caption = message.caption if message.caption else None
                spoiler = message.has_media_spoiler if message.has_media_spoiler else None
                await self.bot.send_video(chat_id=chat_id,
                                          video=video,
                                          caption=caption,
                                          has_spoiler=spoiler)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            if message.photo:
                photo = message.photo[-1].file_id
                caption = message.caption if message.caption else None
                spoiler = message.has_media_spoiler if message.has_media_spoiler else None
                await self.bot.send_photo(chat_id=chat_id,
                                          photo=photo,
                                          caption=caption,
                                          has_spoiler=spoiler)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            if message.audio:
                audio = message.audio.file_id
                await self.bot.send_audio(chat_id=chat_id,
                                          audio=audio)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            if message.document:
                document = message.document.file_id
                caption = message.caption if message.caption else None
                await self.bot.send_document(chat_id=chat_id,
                                             document=document,
                                             caption=caption)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            if message.voice:
                voice = message.voice.file_id
                await self.bot.send_voice(chat_id=chat_id,
                                          voice=voice)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)
            if message.text:
                await self.bot.send_message(chat_id=chat_id,
                                            text=message.text)
                await self.bot.set_message_reaction(chat_id=message.chat.id,
                                                    message_id=message.message_id,
                                                    reaction=reaction)