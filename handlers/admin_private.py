import requests
import asyncio
import logging
import json
from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.types import BufferedInputFile
from common.commands import *
from common.db_settings import *

# from common.subscribe_channels import CHANNEL_ID
from filters.chat_types import *
from keyboards.inline import get_callback_btns
from keyboards.reply import *


logging.basicConfig(level=logging.INFO)


admin_private_router = Router()
admin_private_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_private_router.message(Command("apanel"))
@admin_private_router.message(F.text == "📌Админ панель")
async def apanel(message: types.Message):
    id = message.from_user.id
    if is_superadmin(id):
        await message.answer(
            "Добро пожаловать, уважаемый администратор!👋",
            reply_markup=default_superadmin_keyboard,
        )
    elif is_admin(id):
        await message.answer(
            "Добро пожаловать, уважаемый администратор!👋",
            reply_markup=default_admin_keyboard,
        )


@admin_private_router.message(Command("acommands"))
@admin_private_router.message(F.text == "💬Доступные команды администратора")
async def acommands(message: types.Message, bot: Bot):
    for adm_cmds_list in adm_cmd_list:
        if adm_cmds_list:
            await message.reply(adm_cmds_list)


@admin_private_router.message(Command("ahelp"))
@admin_private_router.message(F.text == "💡Важная информация")
async def ahelp(message: types.Message, bot: Bot):
    await message.reply(
        f"Ниже будет вся полезная информация для администратора.\n\n"
        "Что бы узнать все доступные Вам команды, используйте - /acommands"
    )


@admin_private_router.message(F.text == "💎Главное меню")
async def main_menu(message: types.Message):
    if is_superadmin(message.from_user.id):
        await message.reply(
            f"🔙Вы вернулись в главное меню.", reply_markup=superadmin_user_keyboard
        )
    elif is_admin(message.from_user.id):
        await message.reply(
            f"🔙Вы вернулись в главное меню.", reply_markup=admin_user_keyboard
        )


class GetApiForm(StatesGroup):
    api_url = State()


@admin_private_router.message(Command("getrestapi"))
@admin_private_router.message(F.text == "♨️Получить информацию REST API")
async def get_rest_api(message: types.Message, bot: Bot, state: FSMContext):
    cancel_btn = get_keyboard("Отмена❌")
    await message.answer("Введите ссылку ниже ⬇️", reply_markup=cancel_btn)
    await state.set_state(GetApiForm.api_url)


@admin_private_router.message(StateFilter(GetApiForm.api_url))
async def process_api_url(message: types.Message, state: FSMContext):
    if message.text == "Отмена❌":
        if is_superadmin(message.from_user.id):
            await message.answer(
                "Вы отменили предыдущие действия.",
                reply_markup=default_superadmin_keyboard,
            )
            await state.clear()
            return
        elif is_admin(message.from_user.id):
            await message.answer(
                "Вы отменили предыдущие действия.", reply_markup=default_admin_keyboard
            )
            await state.clear()
            return

    await state.update_data(api_url=message.text)
    await message.reply(
        "Выберите вариант отправки данных ⬇️",
        reply_markup=get_callback_btns(
            btns={
                "Текстом": "text_in_chat",
                "Файлом": "file_in_chat",
            }
        ),
    )


@admin_private_router.callback_query(
    StateFilter(GetApiForm.api_url), F.data == "text_in_chat"
)
async def text_api_url(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    rest_api_url = user_data["api_url"]
    data = await get_api_data(rest_api_url)
    if data:
        results = await format_json_data(data)
        await send_long_message(callback_query.message, results)
    else:
        await callback_query.message.reply(
            "<b>❗❗❗\n\nОшибка при получении данных с API.\n\nПроверьте правильность ссылки.\n\n❗❗❗</b>",
            reply_markup=get_keyboard("🔙Вернуться назад"),
        )

    await state.clear()


@admin_private_router.callback_query(
    StateFilter(GetApiForm.api_url), F.data == "file_in_chat"
)
async def file_api_url(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    rest_api_url = user_data["api_url"]
    data = await get_api_data(rest_api_url)
    if data:
        file_path = await save_data_to_file(data)
        with open(file_path, "rb") as file:
            await callback_query.message.reply_document(
                BufferedInputFile(file.read(), filename="data.json"),
                reply_markup=get_keyboard("🔙Вернуться назад"),
            )
    else:
        await callback_query.message.reply(
            "<b>❗❗❗\n\nОшибка при получении данных с API.\n\nПроверьте правильность ссылки.\n\n❗❗❗</b>",
            reply_markup=get_keyboard("🔙Вернуться назад"),
        )

    await state.clear()


async def get_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        logging.error(f"❗❗❗ Ошибка при получении данных REST API: {e}")
        return None


async def format_json_data(data):
    def format_dict(d, indent=0):
        formatted = ""
        for key, value in d.items():
            if isinstance(value, dict):
                formatted += (
                    " " * indent + f"<b>{key}:</b>\n" + format_dict(value, indent + 4)
                )
            elif isinstance(value, list):
                formatted += (
                    " " * indent
                    + f"<b>{key}:</b>\n"
                    + "".join(format_list(value, indent + 4))
                )
            else:
                formatted += " " * indent + f"<b>{key}:</b> {value}\n"
        return formatted

    def format_list(lst, indent=0):
        formatted = []
        for item in lst:
            if isinstance(item, dict):
                formatted.append(format_dict(item, indent))
            else:
                formatted.append(" " * indent + f"{item}\n")
        return formatted

    if isinstance(data, dict):
        result = [format_dict(data)]
    elif isinstance(data, list):
        result = format_list(data)
    else:
        result = [str(data)]

    return result


async def send_long_message(message: types.Message, texts: list):
    max_length = 4096
    for text in texts:
        for i in range(0, len(text), max_length):
            await message.answer(
                text[i : i + max_length],
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=default_superadmin_keyboard,
            )
            await asyncio.sleep(1.5)


async def save_data_to_file(data):
    file_path = "data.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return file_path


@admin_private_router.message(F.text == "🔙Вернуться назад")
async def back_rest_api(message: types.Message):
    if is_superadmin(message.from_user.id):
        await message.reply(
            f"Вы вернулись назад", reply_markup=default_superadmin_keyboard
        )
    elif is_admin(message.from_user.id):
        await message.reply(f"Вы вернулись назад", reply_markup=default_admin_keyboard)


class SendMessage(StatesGroup):
    text = State()
    channel_id = State()
    confirm_send = State()
    photo = State()


def confirm_btn():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Подтвердить✅")],
            [types.KeyboardButton(text="Пропустить⏭️")],
            [types.KeyboardButton(text="Назад🔙")],
        ],
        resize_keyboard=True,
    )


def get_channel_kb():
    channels = get_channels()
    buttons = [
        types.InlineKeyboardButton(text=channel[1], callback_data=channel[0])
        for channel in channels
    ]
    inline_keyboard = [buttons[i : i + 1] for i in range(0, len(buttons), 1)]
    return types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@admin_private_router.message(Command("send_message"))
@admin_private_router.message(F.text == "🔀Сделать рассылку")
async def cmd_send_message(message: types.Message, state: FSMContext):
    await message.answer("Выберите нужный канал ⬇️", reply_markup=get_channel_kb())
    await state.set_state(SendMessage.channel_id)


@admin_private_router.callback_query(
    StateFilter(SendMessage.channel_id),
    lambda callback_query: callback_query.data.startswith("@"),
)
async def process_channel_selection(
    callback_query: types.CallbackQuery, state: FSMContext
):
    selected_channel = callback_query.data
    await state.update_data(channel_id=selected_channel)
    await callback_query.message.reply(
        "Введите сообщение для отправки в канал 📩", reply_markup=confirm_btn()
    )
    await state.set_state(SendMessage.text)


@admin_private_router.message(StateFilter(SendMessage.text))
async def process_message_text(message: types.Message, state: FSMContext):

    if message.text == "Назад🔙":
        if is_superadmin(message.from_user.id):
            await message.answer(
                "Вы отменили отправку сообщения.",
                reply_markup=default_superadmin_keyboard,
            )
            await state.clear()
        elif is_admin(message.from_user.id):
            await message.answer(
                "Вы отменили отправку сообщения.", reply_markup=default_admin_keyboard
            )
            await state.clear()
    elif message.text == "Пропустить⏭️":
        await state.update_data(text=None)
        await message.answer(
            "Отправьте изображение или пропустите этот шаг ⏭️",
            reply_markup=confirm_btn(),
        )
        await state.set_state(SendMessage.photo)
    else:
        await state.update_data(text=message.text)
        await message.answer(
            "Отправьте изображение или пропустите этот шаг ⏭️",
            reply_markup=confirm_btn(),
        )
        await state.set_state(SendMessage.photo)


@admin_private_router.message(
    StateFilter(SendMessage.photo), F.content_type.in_({"photo", "text"})
)
async def process_message_photo(message: types.Message, state: FSMContext):
    if message.text == "Пропустить⏭️":
        await state.update_data(photo=None)
    elif message.photo:
        photo = message.photo[-1].file_id
        await state.update_data(photo=photo)
    elif message.text == "Назад🔙":
        if is_superadmin(message.from_user.id):
            await message.answer(
                "Вы отменили отправку сообщения.",
                reply_markup=default_superadmin_keyboard,
            )
            await state.clear()
        elif is_admin(message.from_user.id):
            await message.answer(
                "Вы отменили отправку сообщения.", reply_markup=default_admin_keyboard
            )
            await state.clear()
        return

    user_data = await state.get_data()
    channel_id = user_data["channel_id"]
    message_text = user_data["text"]
    photo = user_data.get("photo")

    if photo:
        await message.answer_photo(
            photo=photo,
            caption=f"<b>Вы выбрали канал 💻: </b> {channel_id}\n<b>Текст сообщения 📩: </b> {message_text}\n\nПодтвердите или отмените отправку сообщения",
            reply_markup=confirm_btn(),
        )
    else:
        await message.answer(
            f"<b>Вы выбрали канал 💻: </b> {channel_id}\n<b>Текст сообщения 📩: </b> {message_text}\n\nПодтвердите или отмените отправку сообщения",
            reply_markup=confirm_btn(),
        )

    await state.set_state(SendMessage.confirm_send)


@admin_private_router.message(StateFilter(SendMessage.confirm_send))
async def confirm_send_message(message: types.Message, state: FSMContext, bot: Bot):
    if message.text == "Подтвердить✅":
        user_data = await state.get_data()
        channel_id = user_data["channel_id"]
        message_text = user_data["text"]
        photo = user_data.get("photo")

        try:
            if photo:
                await bot.send_photo(
                    chat_id=channel_id, photo=photo, caption=message_text
                )
            else:
                await bot.send_message(chat_id=channel_id, text=message_text)
            if is_superadmin(message.from_user.id):
                await message.answer(
                    "Сообщение успешно отправлено! ✉️",
                    reply_markup=default_superadmin_keyboard,
                )
            elif is_admin(message.from_user.id):
                await message.answer(
                    "Сообщение успешно отправлено! ✉️",
                    reply_markup=default_admin_keyboard,
                )

        except Exception as e:
            await message.answer(
                f"Ошибка - <b>{e}</b>, обратитесь к руководству бота.",
                reply_markup=default_admin_keyboard,
            )

    elif message.text == "Назад🔙":
        if is_superadmin(message.from_user.id):
            await message.answer(
                "Вы отменили отправку сообщения.",
                reply_markup=default_superadmin_keyboard,
            )
            await state.clear()
        elif is_admin(message.from_user.id):
            await message.answer(
                "Вы отменили отправку сообщения.", reply_markup=default_admin_keyboard
            )
            await state.clear()

    await state.clear()


class SendToAllUsers(StatesGroup):
    text = State()
    image = State()
    confirm_send = State()


def confirm_send_to_all_btn():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Подтвердить✅")],
            [types.KeyboardButton(text="Пропустить⏭️")],
            [types.KeyboardButton(text="Назад🔙")],
        ],
        resize_keyboard=True,
    )


@admin_private_router.message(Command("send_to_all"))
async def send_to_all(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите сообщение для отправки всем пользователям 📧",
        reply_markup=confirm_send_to_all_btn(),
    )
    await state.set_state(SendToAllUsers.text)


@admin_private_router.message(StateFilter(SendToAllUsers.text))
async def process_message_to_all_text(message: types.Message, state: FSMContext):
    if message.text == "Назад🔙":
        await cancel_send_message(message, state)
    elif message.text == "Пропустить⏭️":
        await state.update_data(text=None)
        await message.answer(
            "Отправьте изображение или пропустите этот шаг ⏭️",
            reply_markup=confirm_send_to_all_btn(),
        )
        await state.set_state(SendToAllUsers.image)
    else:
        await state.update_data(text=message.text)
        await message.answer(
            "Отправьте изображение или пропустите этот шаг ⏭️",
            reply_markup=confirm_send_to_all_btn(),
        )
        await state.set_state(SendToAllUsers.image)


@admin_private_router.message(
    StateFilter(SendToAllUsers.image), F.content_type.in_({"photo", "text"})
)
async def process_message_to_all_photo(message: types.Message, state: FSMContext):
    if message.text == "Пропустить⏭️":
        await state.update_data(image=None)
    elif message.photo:
        image = message.photo[-1].file_id
        await state.update_data(image=image)
    elif message.text == "Назад🔙":
        await cancel_send_message(message, state)
        return

    user_data = await state.get_data()
    message_text = user_data.get("text")
    image = user_data.get("image")

    if image:
        await message.answer_photo(
            photo=image,
            caption=f"<b>Текст сообщения 📩: </b> {message_text}\n\nПодтвердите или отмените отправку сообщения",
            reply_markup=confirm_send_to_all_btn(),
        )
    else:
        await message.answer(
            f"<b>Текст сообщения 📩: </b> {message_text}\n\nПодтвердите или отмените отправку сообщения",
            reply_markup=confirm_send_to_all_btn(),
        )

    await state.set_state(SendToAllUsers.confirm_send)


@admin_private_router.message(StateFilter(SendToAllUsers.confirm_send))
async def confirm_send_to_all_message(
    message: types.Message, state: FSMContext, bot: Bot
):
    if message.text == "Подтвердить✅":
        user_data = await state.get_data()
        message_text = user_data.get("text")
        image = user_data.get("image")

        all_users = get_all_users()
        success_count = 0
        fail_count = 0

        for user_id in all_users:
            try:
                if image:
                    await bot.send_photo(
                        chat_id=user_id, photo=image, caption=message_text
                    )
                else:
                    await bot.send_message(chat_id=user_id, text=message_text)
                success_count += 1
            except Exception as e:
                fail_count += 1

        if is_superadmin(message.from_user.id):
            await message.answer(
                f"Сообщение успешно отправлено {success_count} пользователям! {fail_count} пользователям отправка не удалась.",
                reply_markup=default_superadmin_keyboard,
            )
        elif is_admin(message.from_user.id):
            await message.answer(
                f"Сообщение успешно отправлено {success_count} пользователям! {fail_count} пользователям отправка не удалась.",
                reply_markup=default_admin_keyboard,
            )

    elif message.text == "Назад🔙":
        await cancel_send_message(message, state)

    await state.clear()


async def cancel_send_message(message: types.Message, state: FSMContext):
    if is_superadmin(message.from_user.id):
        await message.answer(
            "Вы отменили отправку сообщения.", reply_markup=default_superadmin_keyboard
        )
    elif is_admin(message.from_user.id):
        await message.answer(
            "Вы отменили отправку сообщения.", reply_markup=default_admin_keyboard
        )
    await state.clear()
