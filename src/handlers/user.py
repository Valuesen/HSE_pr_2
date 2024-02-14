from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext

from Texts.texts import MESSAGES

from src.keyboards import keyboards
from src.services.sql import DataBase
from src.config import database_path
from src.states.user_states import AddServiceStates, DeleteService, GetPassword

db = DataBase(database_path)
router = Router()


@router.message(F.text == '🔑Хранилище🔑')  # Обрабатывает кнопку 🔧Управление сервисами🔧
async def pwd_manage(message: Message):
    await message.answer(MESSAGES["pwd_manage"], reply_markup=keyboards.pwd_menage_keyboard())


@router.message(F.text == '📋Список моих сервисов📋')  # Обрабатывает кнопку 🔧Управление сервисами🔧
async def pwd_manage(message: Message, state: FSMContext):
    data = await db.get_value('id', message.from_user.id)
    if await db.user_in_base(message.from_user.id):
        if data[6] == 1:
            await state.set_state(GetPassword.password)
            await message.answer('Введите пароль ЛК:')
        else:
            data = data[4].split('/')
            s = []
            for i in data:
                s.append(i.split(':')[0])
            if s == ['']:
                await message.answer('Нет доступных сервисов\nДобавите их, используя кнопку ✅Добавить✅')
            else:
                await message.answer('Сервисы:', reply_markup=keyboards.services_main_keyboard(s))
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '👤 Личный кабинет 👤')  # Обрабатывает кнопку 👤Аккаунт👤
async def account(message: Message):
    if await db.user_in_base(message.from_user.id):
        user = await db.get_value('id', message.from_user.id)
        x = user[4].split("/")
        await message.answer(f'Имя: {user[1]}\n'
                             f'Запрос пароля ЛК: {"Вкл.🟢" if user[6] == 1 else "Выкл.🔴"}\n'
                             f'Уведомления: {"Вкл.🟢" if user[5] == 1 else "Выкл.🔴"}\n'
                             f'Смена пароля: каждые {user[3]} дн.\n'
                             f'Сервисов добавлено: {0 if x == [""] else len(x)}\n',

                             reply_markup=keyboards.account_keyboard())
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '⬅Главное меню')  # Обрабатывает кнопку ⬅Назад
async def back(message: Message):
    await message.answer('Главное меню:', reply_markup=keyboards.main_menu_keyboard())


@router.message(F.text == '✅Добавить✅')  # Обрабатывает кнопку ✅Добавить сер.✅
async def add_service(message: Message, state: FSMContext):
    if await db.user_in_base(message.from_user.id):
        await state.set_state(AddServiceStates.service_name)
        await message.answer('Напишите название сервиса,\nпароль которого необходимо сохранить.\n'
                             'Например: mail.ru\n'
                             'Не используйте символы / и :', reply_markup=None)
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '❌Удалить❌')  # Обрабатывает кнопку ❌Удалить сер.❌
async def del_service(message: Message, state: FSMContext):
    if await db.user_in_base(message.from_user.id):
        user = await db.get_value('id', message.from_user.id)
        if user[6]:
            await message.answer('Введите пароль ЛК:')
            await state.set_state(DeleteService.password)
        else:
            data = user[4].split('/')
            s = []
            for i in data:
                s.append(i.split(':')[0])
            if s == ['']:
                await message.answer('Нет доступных сервисов\nДобавите их, используя кнопку ✅Добавить✅')
            else:
                await message.answer('Выберите сервис:', reply_markup=keyboards.services_delete_keyboard(s))

    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.sticker)  # Обрабатывает неизвесный текст
async def other_messages(message: Message):
    await message.bot.send_sticker(message.chat.id,
                                   message.sticker.file_id)


@router.message()  # Обрабатывает неизвесный текст
async def other_messages(message: Message):
    await message.answer('Для навигации используйте кнопки')
