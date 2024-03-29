from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard():  # Клавиатура главного меню
    menu_keyboard = [
        [types.KeyboardButton(text="🔑Хранилище🔑")],
        [types.KeyboardButton(text="👤 Личный кабинет 👤")]
    ]

    menu_keyboard = types.ReplyKeyboardMarkup(keyboard=menu_keyboard,
                                              resize_keyboard=True,
                                              input_field_placeholder="Главное меню")
    return menu_keyboard


def random_gen_keyboard():  # Клавиатура главного меню
    gen_keyboard = [
        [types.KeyboardButton(text="🎲Генирация пароля🎲")]
    ]

    gen_keyboard = types.ReplyKeyboardMarkup(keyboard=gen_keyboard,
                                             resize_keyboard=True,
                                             input_field_placeholder="Пароль")
    return gen_keyboard


def pass_keyboard():  # Клавиатура главного меню
    buttons = [
        [types.KeyboardButton(text="🔽Пропустить🔽")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Пароль")
    return keyboard


def pwd_menage_keyboard():  # Клавиатура меню управления сервисами
    buttons = [
        [types.KeyboardButton(text="📋Список моих сервисов📋")],
        [types.KeyboardButton(text="✅Добавить✅"), types.KeyboardButton(text="❌Удалить❌")],
        [types.KeyboardButton(text="⬅Главное меню")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Управление паролями")
    return keyboard


def account_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="⚙️ Настроить ⚙️",
        callback_data="edit_profile")
    )

    builder.add(types.InlineKeyboardButton(
        text="❌Закрыть❌",
        callback_data="close_profile_menu")
    )
    builder.adjust(1)
    return builder.as_markup()


def edit_account_keyboard(user):
    alerts_text = 'Включить уведомления' if user[5] == 0 else 'Выключить уведомления'
    pwd_text = 'Включить запрос пароля ЛК' if user[6] == 0 else 'Выключить запрос пароля ЛК'

    buttons = [
        [types.InlineKeyboardButton(text="Изменить имя", callback_data='edit_name')],
        [types.InlineKeyboardButton(text="Изменить пароль ЛК", callback_data='edit_passwd')],
        [types.InlineKeyboardButton(text=pwd_text, callback_data='edit_passwd_req')],
        [types.InlineKeyboardButton(text=alerts_text, callback_data='edit_alerts')],
        [types.InlineKeyboardButton(text="Периодичность смены пароля", callback_data='edit_period')],
        [types.InlineKeyboardButton(text="Удалить аккаунт", callback_data='del_account')],
        [types.InlineKeyboardButton(text="❌Закрыть❌", callback_data='close_profile_menu')]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def verification_keyboard(func):
    builder = None
    if func == 'add':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Добавить✅",
            callback_data="add_service")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Отменить❌",
            callback_data="cancel")
        )
    elif func == 'edit':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Обновить✅",
            callback_data="edit_service")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Отменить❌",
            callback_data="cancel")
        )
    elif func == 'delete':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Оставить✅",
            callback_data="cancel")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Удалить❌",
            callback_data="delete_service")
        )

    elif func == 'edit_name':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Изменить✅",
            callback_data="edit_name_final")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Отменить❌",
            callback_data="cancel")
        )
    elif func == 'del_account':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Оставить✅",
            callback_data="cancel")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Удалить❌",
            callback_data="del_account_final")
        )
    elif func == 'edit_ac_pwd':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Сменить✅",
            callback_data="edit_ac_true")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Оставить❌",
            callback_data="cancel")
        )
    elif func == 'edit_login':
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="✅Сменить✅",
            callback_data="edit_login_true")
        )

        builder.add(types.InlineKeyboardButton(
            text="❌Оставить❌",
            callback_data="cancel")
        )
    builder.adjust(2)
    return builder.as_markup()


def services_main_keyboard(services):
    builder = InlineKeyboardBuilder()
    for i in services:
        builder.add(types.InlineKeyboardButton(
            text=i,
            callback_data=f'service:{i}')
        )

    builder.add(types.InlineKeyboardButton(
        text="❌Закрыть❌",
        callback_data="close")
    )
    builder.adjust(1)

    return builder.as_markup()


def service_keyboard(service):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Изменить логин",
        callback_data=f"change_login:{service}")
    )
    builder.add(types.InlineKeyboardButton(
        text="Изменить пароль",
        callback_data=f"change_password:{service}")
    )
    builder.add(types.InlineKeyboardButton(
        text="⬅К списку сервисов",
        callback_data=f"services_keyboard")
    )
    builder.add(types.InlineKeyboardButton(
        text="❌Закрыть❌",
        callback_data="close")
    )
    builder.adjust(1)

    return builder.as_markup()


def apsched_keyboad():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="✅Сменить✅",
        callback_data="edit_service_password")
    )
    builder.add(types.InlineKeyboardButton(
        text="❌Закрыть❌",
        callback_data="cancel")
    )
    builder.adjust(1)

    return builder.as_markup()


def services_edit_keyboard(services):
    builder = InlineKeyboardBuilder()

    for i in services:
        builder.add(types.InlineKeyboardButton(
            text=i,
            callback_data=f'edit:{i}')
        )
    builder.add(types.InlineKeyboardButton(
        text="❌Отменить❌",
        callback_data="cancel")
    )
    builder.adjust(1)

    return builder.as_markup()


def services_delete_keyboard(services):
    builder = InlineKeyboardBuilder()

    for i in services:
        builder.add(types.InlineKeyboardButton(
            text=i,
            callback_data=f'del:{i}')
        )
    builder.add(types.InlineKeyboardButton(
        text="❌Отменить❌",
        callback_data="cancel")
    )
    builder.adjust(1)

    return builder.as_markup()


def start_keyboard():
    buttons = [
        [types.KeyboardButton(text="/start")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Необходима регистрация")
    return keyboard


def cancel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="↩️Отменить↩️",
        callback_data="cancel")
    )
    builder.adjust(1)

    return builder.as_markup()
