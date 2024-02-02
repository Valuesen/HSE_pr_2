from datetime import date

from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext

from Texts.texts import MESSAGES

from src.keyboards import keyboards
from src.services.sql import DataBase
from src.config import database_path
from src.states.user_states import AddServiceStates

db = DataBase(database_path)
router = Router()


@router.message(F.text == '🔧Управление сервисами🔧')  # Обрабатывает кнопку 🔧Управление сервисами🔧
async def pwd_manage(message: Message):
    await message.answer(MESSAGES["pwd_manage"], reply_markup=keyboards.pwd_menage_keyboard())


@router.message(F.text == '📋Список сервисов📋')  # Обрабатывает кнопку 🔧Управление сервисами🔧
async def pwd_manage(message: Message):
    data = await db.get_value('id', message.from_user.id)
    services = data[4].split('/')
    text = []
    for i in services:
        data_in_serv = i.split(":")
        time = data_in_serv[2].split('-')
        k = str(date(int(time[0]), int(time[1]), int(time[2])) - date.today())
        if k == '0:00:00':
            text.append(f"{data_in_serv[0]}: 60 дней")
        else:
            k = int(k.replace(' days, 0:00:00', ''))
            text.append(f"{data_in_serv[0]}: {60+k} дней")
    print(text)
    await message.answer('\n'.join(text), reply_markup=keyboards.pwd_menage_keyboard())


@router.message(F.text == '👤Аккаунт👤')  # Обрабатывает кнопку 👤Аккаунт👤
async def account(message: Message):
    if await db.user_in_base(message.from_user.id):
        data = await db.get_value('id', message.from_user.id)
        await message.answer(f'Имя: {data[1]}\nСервисов: {len(data[4].split("/"))}',
                             reply_markup=keyboards.account_keyboard())
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '⬅Назад')  # Обрабатывает кнопку ⬅Назад
async def back(message: Message):
    await message.answer('Главное меню:', reply_markup=keyboards.main_menu_keyboard())


@router.message(F.text == '✅Добавить сер.✅')  # Обрабатывает кнопку ✅Добавить сер.✅
async def add_service(message: Message, state: FSMContext):
    await message.answer('Напишите название сервиса\n(Не используйте : и /):', reply_markup=None)
    await state.set_state(AddServiceStates.service_name)


@router.message(F.text == '❌Удалить сер.❌')  # Обрабатывает кнопку ❌Удалить сер.❌
async def del_service(message: Message):
    if await db.user_in_base(message.from_user.id):
        data = await db.get_value('id', message.from_user.id)
        data = data[4].split('/')
        s = []
        for i in data:
            s.append(i.split(':')[0])
        await message.answer('Выберите сервис:', reply_markup=keyboards.services_delete_keyboard(s))
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '🔧Изменить пароль🔧')  # Обрабатывает кнопку 🔧Изменить пароль🔧
async def del_service(message: Message):
    if await db.user_in_base(message.from_user.id):
        data = await db.get_value('id', message.from_user.id)
        data = data[4].split('/')
        s = []
        for i in data:
            s.append(i.split(':')[0])
        await message.answer('Выберите сервис:', reply_markup=keyboards.services_edit_keyboard(s))
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '📥Получить пароль📥')  # Обрабатывает кнопку 📥Получить пароль📥
async def del_service(message: Message):
    if await db.user_in_base(message.from_user.id):
        data = await db.get_value('id', message.from_user.id)
        data = data[4].split('/')
        s = []
        for i in data:
            s.append(i.split(':')[0])
        await message.answer('Выберите сервис:', reply_markup=keyboards.services_keyboard(s))
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message()  # Обрабатывает неизвесный текст
async def other_messages(message: Message):
    await message.answer('Для навигации используйте кнопки')
