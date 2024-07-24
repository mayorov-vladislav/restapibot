<<<<<<< HEAD
from aiogram import types
from aiogram.filters import Filter
from common.db_settings import *


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return is_admin(message.from_user.id)


class IsSuperAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        return is_superadmin(message.from_user.id)
=======
from aiogram import Router, Bot, types
from aiogram.filters import Filter
from common.subscribe_channels import CHANNEL_ID


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admin_list


async def is_user_admin(user_id: int, bot: Bot) -> bool:
    return any(
        [
            (await bot.get_chat_member(chat_id, user_id)).status
            in ["administrator", "creator"]
            for chat_id in CHANNEL_ID
        ]
    )
>>>>>>> cbbc20bf4e1b6bbe24b0e15d6f77ca651094e540
