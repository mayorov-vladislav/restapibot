from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
):
    """
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона",
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    """

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))

        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True, input_field_placeholder=placeholder
    )


default_admin_keyboard = get_keyboard(
    "💎Главное меню",
    "♨️Получить информацию REST API",
    "🔀Сделать рассылку",
    "💡Важная информация",
    "💬Доступные команды администратора",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 2),
)


default_superadmin_keyboard = get_keyboard(
    "💎Главное меню",
    "♨️Получить информацию REST API",
    "🔀Сделать рассылку",
    "💡Важная информация",
    "💬Доступные команды администратора",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(
        2,
        2,
    ),
)


default_user_keyboard = get_keyboard(
    "💡Полезная информация",
    "💬Доступные команды",
    "Кнопка",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 1),
)


admin_user_keyboard = get_keyboard(
    "💡Полезная информация",
    "💬Доступные команды",
    "📌Админ панель",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 1),
)


superadmin_user_keyboard = get_keyboard(
    "💡Полезная информация",
    "💬Доступные команды",
    "🎃Панель супер администратора",
    "📌Админ панель",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 2),
)


superadmin_keyboard = get_keyboard(
    "💎Главное меню",
    "🔰Управление администрацией",
    "📢Управление каналами",
    "💬Доступные команды супер администратора",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 2),
)


admin_control = get_keyboard(
    "🎃Панель супер администратора",
    "📋Список администрации",
    "➕Добавить администратора",
    "➖Удалить администратора",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 2),
)

channel_control = get_keyboard(
    "🎃Панель супер администратора",
    "📋Список каналов",
    "➕Добавить канал",
    "➖Удалить канал",
    placeholder="Выберите нужный Вам вариант ниже.",
    sizes=(2, 2),
)
