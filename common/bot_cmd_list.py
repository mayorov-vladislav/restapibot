<<<<<<< HEAD
from aiogram.types import BotCommand


private_user_cmd = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="help", description="Полезная информация"),
    BotCommand(command="commands", description="Все команды пользователя"),
]

private_admin_cmd = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="help", description="Полезная информация"),
    BotCommand(command="commands", description="Все команды пользователя"),
    BotCommand(command="apanel", description="Меню администратора"),
    BotCommand(command="ahelp", description="Важная информация администрации"),
    BotCommand(command="acommands", description="Все команды администрации"),
    BotCommand(command="getrestapi", description="Сделать рассылку по чатам"),
]
=======
from aiogram.types import BotCommand
from aiogram import types, Bot
from filters.chat_types import is_user_admin


private_user_cmd = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="help", description="Полезная информация"),
    BotCommand(command="commands", description="Все команды пользователя"),
]

private_admin_cmd = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="help", description="Полезная информация"),
    BotCommand(command="commands", description="Все команды пользователя"),
    BotCommand(command="apanel", description="Меню администратора"),
    BotCommand(command="ahelp", description="Важная информация администрации"),
    BotCommand(command="acommands", description="Все команды администрации"),
    BotCommand(command="getrestapi", description="Сделать рассылку по чатам"),
]
>>>>>>> cbbc20bf4e1b6bbe24b0e15d6f77ca651094e540
