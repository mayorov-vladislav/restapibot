from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command
from filters.chat_types import ChatTypeFilter
from common.commands import *
from keyboards.reply import *
from filters.chat_types import *
from common.db_settings import *


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, bot: Bot):
    id = message.from_user.id
    username = message.from_user.username
    add_user(id, username)

    if is_superadmin(id):
        for superadm_cmd in superadmin_user_cmd_list:
            await message.reply(
                f"{superadm_cmd}",
                reply_markup=superadmin_user_keyboard,
            )
    elif is_admin(id):
        for adm_cmd in admin_user_cmd_list:
            await message.reply(
                f"{adm_cmd}",
                reply_markup=admin_user_keyboard,
            )
    else:
        for user_cmd in cmd_list:
            await message.reply(
                f"{user_cmd}",
                reply_markup=default_user_keyboard,
            )


@user_private_router.message(Command("commands"))
@user_private_router.message(F.text == "💬Доступные команды")
async def start_cmd(message: types.Message, bot: Bot):
    for user_cmd in cmd_list:
        await message.reply(f"{user_cmd}")


@user_private_router.message(Command("help"))
@user_private_router.message(F.text == "💡Полезная информация")
async def ahelp(message: types.Message, bot: Bot):
    await message.reply(
        f"Ниже будет вся полезная информация для пользователей.\n\n"
        "Что бы узнать все доступные Вам команды, используйте - /commands"
    )


@user_private_router.message(Command("get_id"))
async def get_id(message: types.Message):
    await message.reply(f"Your Telegram ID: {message.from_user.id}")
