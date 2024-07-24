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
