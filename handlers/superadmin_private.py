import logging
from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from common.commands import *
from common.db_settings import *
from filters.chat_types import *
from keyboards.inline import *
from keyboards.reply import *


logging.basicConfig(level=logging.INFO)


superadmin_private_router = Router()
superadmin_private_router.message.filter(ChatTypeFilter(["private"]), IsSuperAdmin())


@superadmin_private_router.message(Command("spanel"))
@superadmin_private_router.message(F.text == "🎃Панель супер администратора")
async def superadmin_panel(message: types.Message):
    await message.answer(
        f"Добро пожаловать, уважаемый супер администратор!",
        reply_markup=superadmin_keyboard,
    )


@superadmin_private_router.message(F.text == "🔰Управление администрацией")
async def admin_managment(message: types.Message):
    await message.answer(
        f"Вы вошли в панель управления администрацией.", reply_markup=admin_control
    )


@superadmin_private_router.message(F.text == "📋Список администрации")
async def admin_list(message: types.Message):
    choice_admin = get_keyboard("♟️Администраторы", "👑Супер администраторы", "🔙Назад")
    await message.answer("Выберите нужную вам категорию.", reply_markup=choice_admin)


@superadmin_private_router.message(F.text == "🔙Назад")
async def return_admin_control(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись назад", reply_markup=admin_control)
    await state.clear()


@superadmin_private_router.message(Command("admlist"))
@superadmin_private_router.message(F.text == "♟️Администраторы")
async def get_admin_list(message: types.Message):
    admins = get_admins()

    response = "<b>Список администрации: </b>\n"
    if admins:
        for id, username, name, surname in admins:
            response += f"👤 ID: {id} | Username: ({username}) | Name: {name} | Surname: {surname}\n"
    else:
        response += "Список администрации пуст."

    await message.answer(response)


@superadmin_private_router.message(Command("sadmlist"))
@superadmin_private_router.message(F.text == "👑Супер администраторы")
async def get_superadmin_list(message: types.Message):
    superadmins = get_superadmins()

    response = "<b>Список супер администрации: </b>\n"
    if superadmins:
        for id, username, name, surname in superadmins:
            response += f"👤 ID: {id} | Username: ({username}) | Name: {name} | Surname: {surname}\n"
    else:
        response += "Список супер администрации пуст."

    await message.answer(response)


@superadmin_private_router.message(Command("scommands"))
@superadmin_private_router.message(F.text == "💬Доступные команды супер администратора")
async def scommands(message: types.Message):
    for superadm_cmds_list in superadm_cmd_list:
        if superadm_cmds_list:
            await message.reply(superadm_cmds_list)


class AddAdmin(StatesGroup):
    user_choice = State()
    admin_id = State()
    admin_username = State()
    admin_name = State()
    admin_surname = State()


cancel_add = get_keyboard("✖️Отменить добавление")


@superadmin_private_router.message(Command("add_admin"))
@superadmin_private_router.message(F.text == "➕Добавить администратора")
async def add_administrator(message: types.Message, state: FSMContext):
    choice_add_admin_kb = get_keyboard(
        "🖊️Добавить администратора",
        "🔙Назад",
    )
    await message.answer(
        "Подтвердите добавление администратора.", reply_markup=choice_add_admin_kb
    )
    await state.set_state(AddAdmin.user_choice)


@superadmin_private_router.message(AddAdmin.user_choice)
async def process_user_choice(message: types.Message, state: FSMContext):
    user_choice = message.text
    await state.update_data(user_choice=user_choice)

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление администратора.", reply_markup=admin_control
        )
        await state.clear()

    else:
        if user_choice == "🖊️Добавить администратора":
            await message.answer(
                "Пожалуйста, введите ID пользователя ниже...", reply_markup=cancel_add
            )
            await state.set_state(AddAdmin.admin_id)
        elif user_choice == "🔙Назад":
            await message.answer("Вы вернулись назад", reply_markup=admin_control)
            await state.clear()
        else:
            await message.answer("Неверный выбор!")
            await state.set_state(AddAdmin.user_choice)
            await state.clear()


@superadmin_private_router.message(AddAdmin.admin_id)
async def process_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    admins = get_admins()

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление администратора.", reply_markup=admin_control
        )
        await state.clear()

    else:
        if any(admin[0] == admin_id for admin in admins):
            await message.answer(
                "Пользователь уже является администратором.", reply_markup=admin_control
            )
            await state.clear()
        else:
            await state.update_data(admin_id=admin_id)
            await message.answer(
                "Пожалуйста, введите Username пользователя...", reply_markup=cancel_add
            )
            await state.set_state(AddAdmin.admin_username)


@superadmin_private_router.message(AddAdmin.admin_username)
async def process_admin_username(message: types.Message, state: FSMContext):
    admin_username = message.text
    admins = get_admins()

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление администратора.", reply_markup=admin_control
        )
        await state.clear()

    else:
        if any(admin[1] == admin_username for admin in admins):
            await message.answer(
                "Пользователь уже является администратором.", reply_markup=admin_control
            )
            await state.clear()
        else:
            await state.update_data(admin_username=admin_username)
            await message.answer(
                "Пожалуйста, введите имя пользователя...", reply_markup=cancel_add
            )
            await state.set_state(AddAdmin.admin_name)


@superadmin_private_router.message(AddAdmin.admin_name)
async def process_admin_name(message: types.Message, state: FSMContext):

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление администратора.", reply_markup=admin_control
        )
        await state.clear()

    else:
        admin_name = message.text
        await state.update_data(admin_name=admin_name)
        await message.answer(
            "Пожалуйста, введите фамилию пользователя...", reply_markup=cancel_add
        )
        await state.set_state(AddAdmin.admin_surname)


@superadmin_private_router.message(AddAdmin.admin_surname)
async def process_admin_surname(message: types.Message, state: FSMContext):
    admin_surname = message.text
    user_data = await state.get_data()
    admins = get_admins()

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление администратора.", reply_markup=admin_control
        )
        await state.clear()

    else:
        if any(
            admin[0] == user_data.get("admin_id")
            or admin[1] == user_data.get("admin_username")
            for admin in admins
        ):
            await message.answer(
                "Пользователь уже является администратором.", reply_markup=admin_control
            )
            await state.clear()

        else:
            add_admin(
                user_id=user_data.get("admin_id"),
                username=user_data.get("admin_username"),
                name=user_data.get("admin_name"),
                surname=admin_surname,
            )
            await message.answer(
                "Администратор успешно добавлен.", reply_markup=admin_control
            )
            await state.clear()


class DelAdmin(StatesGroup):
    admin_id = State()
    confirm_send = State()


confirm_btn = get_keyboard("☑️Подтвердить", "✖️Отмена")


@superadmin_private_router.message(Command("del_admin"))
@superadmin_private_router.message(F.text == "➖Удалить администратора")
async def delete_admin(message: types.Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите ID администратора, которого хотите удалить.",
        reply_markup=confirm_btn,
    )
    await state.set_state(DelAdmin.admin_id)


@superadmin_private_router.message(DelAdmin.admin_id)
async def process_del_admin(message: types.Message, state: FSMContext):
    if message.text == "✖️Отмена":
        await message.answer(
            "Вы отменили удаление администратора.", reply_markup=admin_control
        )
        await state.clear()
    else:
        try:
            admin_id = int(message.text.strip())
            await message.answer(
                f"Вы действительно хотите удалить администратора с ID {admin_id}?",
                reply_markup=confirm_btn,
            )
            await state.update_data(admin_id=admin_id)
            await state.set_state(DelAdmin.confirm_send)
        except ValueError:
            await message.reply(
                "ID пользователя должно быть числом.", reply_markup=confirm_btn
            )


@superadmin_private_router.message(StateFilter(DelAdmin.confirm_send))
async def confirm_del_admin(message: types.Message, state: FSMContext):
    if message.text == "✖️Отмена":
        await message.answer(
            "Вы отменили удаление администратора.", reply_markup=admin_control
        )
        await state.clear()

    elif message.text == "☑️Подтвердить":
        state_data = await state.get_data()
        admin_id = state_data.get("admin_id")

        if admin_id in [admin[0] for admin in get_admins()]:
            del_admin(admin_id)
            await message.answer("Администратор удален.", reply_markup=admin_control)
        else:
            await message.answer(
                "Пользователь не является администратором.", reply_markup=admin_control
            )

        await state.clear()


@superadmin_private_router.message(F.text == "📢Управление каналами")
async def admin_managment(message: types.Message):
    await message.answer(
        f"Вы вошли в панель управления каналами.", reply_markup=channel_control
    )


@superadmin_private_router.message(Command("channel_list"))
@superadmin_private_router.message(F.text == "📋Список каналов")
async def get_channel(message: types.Message):
    channels = get_channels()

    response = "<b>Список каналов: </b>\n"
    if channels:
        for channel_id, title in channels:
            response += f"📃 Channel ID: ({channel_id}) | Title: {title}\n"
    else:
        response += "Список каналов пуст."

    await message.answer(response)


class AddChannel(StatesGroup):
    channel_link = State()
    channel_title = State()
    confirm_add_channel = State()


cancel_add_channel = get_keyboard("✖️Отменить добавление")


@superadmin_private_router.message(Command("add_channel"))
@superadmin_private_router.message(F.text == "➕Добавить канал")
async def add_channel_command(message: types.Message, state: FSMContext):
    choice_add_channel_kb = get_keyboard(
        "📍Добавить канал",
        "🔙Назад",
    )
    await message.answer(
        "Подтвердите добавление канала.", reply_markup=choice_add_channel_kb
    )
    await state.set_state(AddChannel.confirm_add_channel)


@superadmin_private_router.message(AddChannel.confirm_add_channel)
async def process_confirm_add_channel(message: types.Message, state: FSMContext):
    confirm_add_channel = message.text
    await state.update_data(confirm_add_channel=confirm_add_channel)

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление канала.", reply_markup=channel_control
        )
        await state.clear()
    elif confirm_add_channel == "📍Добавить канал":
        await message.answer(
            "Пожалуйста, введите ссылку на канал ниже...",
            reply_markup=cancel_add_channel,
        )
        await state.set_state(AddChannel.channel_link)
    elif confirm_add_channel == "🔙Назад":
        await message.answer("Вы вернулись назад", reply_markup=channel_control)
        await state.clear()
    else:
        await message.answer("Неверный выбор!")
        await state.set_state(AddChannel.confirm_add_channel)
        await state.clear()


@superadmin_private_router.message(AddChannel.channel_link)
async def process_channel_link(message: types.Message, state: FSMContext):
    channel_link = message.text
    channels = get_channels()

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление канала.", reply_markup=channel_control
        )
        await state.clear()
    elif any(channel[0] == channel_link for channel in channels):
        await message.answer("Канал уже добавлен.", reply_markup=channel_control)
        await state.clear()
    else:
        await state.update_data(channel_link=channel_link)
        await message.answer(
            "Пожалуйста, введите название канала...", reply_markup=cancel_add_channel
        )
        await state.set_state(AddChannel.channel_title)


@superadmin_private_router.message(AddChannel.channel_title)
async def process_channel_title(message: types.Message, state: FSMContext):
    channel_title = message.text
    user_data = await state.get_data()
    channels = get_channels()

    if message.text == "✖️Отменить добавление":
        await message.answer(
            "Вы отменили добавление канала.", reply_markup=channel_control
        )
        await state.clear()
    elif any(
        channel[0] == user_data.get("channel_link") or channel[1] == channel_title
        for channel in channels
    ):
        await message.answer("Канал уже добавлен.", reply_markup=channel_control)
        await state.clear()
    else:
        add_channel(
            channel_link=user_data.get("channel_link"),
            title=channel_title,
        )
        await message.answer("Канал успешно добавлен.", reply_markup=channel_control)
        await state.clear()


class DelChannel(StatesGroup):
    channel_link = State()
    confirm_channel_send = State()


confirm_del_channle_btn = get_keyboard("☑️Подтвердить", "✖️Отмена")


@superadmin_private_router.message(Command("del_channel"))
@superadmin_private_router.message(F.text == "➖Удалить канал")
async def delete_admin(message: types.Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите ссылку на канал, который хотите удалить.",
        reply_markup=confirm_del_channle_btn,
    )
    await state.set_state(DelChannel.channel_link)


@superadmin_private_router.message(DelChannel.channel_link)
async def process_del_channel(message: types.Message, state: FSMContext):
    if message.text == "✖️Отмена":
        await message.answer(
            "Вы отменили удаление канала.", reply_markup=channel_control
        )
        await state.clear()
    else:
        try:
            channel_link = message.text.strip()
            await message.answer(
                f"Вы действительно хотите удалить канал {channel_link}?",
                reply_markup=confirm_del_channle_btn,
            )
            await state.update_data(channel_link=channel_link)
            await state.set_state(DelChannel.confirm_channel_send)
        except ValueError as e:
            await message.reply(
                "Ошибка: {e}. Обратитесь к руководству бота.",
                reply_markup=confirm_del_channle_btn,
            )


@superadmin_private_router.message(StateFilter(DelChannel.confirm_channel_send))
async def confirm_del_channel(message: types.Message, state: FSMContext):
    if message.text == "✖️Отмена":
        await message.answer(
            "Вы отменили удаление канала.", reply_markup=channel_control
        )
        await state.clear()

    elif message.text == "☑️Подтвердить":
        state_data = await state.get_data()
        channel_link = state_data.get("channel_link")

        if channel_link in [channel[0] for channel in get_channels()]:
            del_channel(channel_link)
            await message.answer("Канал удален.", reply_markup=channel_control)
        else:
            await message.answer(
                "Данный канал отсутствует в списке каналов.",
                reply_markup=channel_control,
            )

        await state.clear()
