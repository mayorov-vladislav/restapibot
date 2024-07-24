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
