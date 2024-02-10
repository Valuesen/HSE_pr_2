from datetime import date

from aiogram.types import Message
from aiogram import F
from aiogram import Router
from aiogram.fsm.context import FSMContext

from Texts.texts import MESSAGES

from src.keyboards import keyboards
from src.services.sql import DataBase
from src.config import database_path
from src.states.user_states import AddServiceStates, GetPassword, EditPassword, DeleteService

db = DataBase(database_path)
router = Router()


@router.message(F.text == '🔑Управление сервисами🔑')  # Обрабатывает кнопку 🔧Управление сервисами🔧
async def pwd_manage(message: Message):
    await message.answer(MESSAGES["pwd_manage"], reply_markup=keyboards.pwd_menage_keyboard())


@router.message(F.text == '📋Список моих сервисов📋')  # Обрабатывает кнопку 🔧Управление сервисами🔧
async def pwd_manage(message: Message):
    data = await db.get_value('id', message.from_user.id)
    if data[4] == '':
        await message.answer('Нет доступных сервисов\nДобавте их, используя\nкнопку ✅Добавить сер.✅')
        return 1
    services = data[4].split('/')
    text = []
    for i in services:
        data_in_serv = i.split(":")
        time = data_in_serv[2].split('-')
        k = str(date(int(time[0]), int(time[1]), int(time[2])) - date.today())
        if k == '0:00:00':
            text.append(f"{data_in_serv[0]}: {data[3]} дн. до смены пароля")
        else:
            k = int(k.split(' ')[0])
            if data[3]+k > 0:
                text.append(f"{data_in_serv[0]}: {data[3]+k} дн. до смены пароля")
            else:
                text.append(f"{data_in_serv[0]}: пора менять")
    await message.answer('\n'.join(text), reply_markup=keyboards.pwd_menage_keyboard())


@router.message(F.text == '👤АККАУНТ')  # Обрабатывает кнопку 👤Аккаунт👤
async def account(message: Message):
    if await db.user_in_base(message.from_user.id):
        user = await db.get_value('id', message.from_user.id)
        x = user[4].split("/")
        await message.answer(f'Имя: {user[1]}\nСервисов добавлено: {0 if x == [""] else len(x)}\nПериод: {user[3]} д.\n'
                             f'Уведомления: {"Включены🟢" if user[5] == 1 else "Выключены🔴"}\n'
                             f'Запрос пароля: {"Включен🟢" if user[6] == 1 else "Выключен🔴"}',
                             reply_markup=keyboards.account_keyboard())
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '⬅Назад')  # Обрабатывает кнопку ⬅Назад
async def back(message: Message):
    await message.answer('Главное меню:', reply_markup=keyboards.main_menu_keyboard())


@router.message(F.text == '✅Добавить сервис✅')  # Обрабатывает кнопку ✅Добавить сер.✅
async def add_service(message: Message, state: FSMContext):
    await message.answer('Напишите название сервиса,\nпароль которого необходимо сохранить.\n'
                         'Например: mail.ru\n'
                         'Не используйте символы / и :', reply_markup=None)
    await state.set_state(AddServiceStates.service_name)


@router.message(F.text == '❌Удалить сервис❌')  # Обрабатывает кнопку ❌Удалить сер.❌
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
            await message.answer('Выберите сервис:', reply_markup=keyboards.services_delete_keyboard(s))

    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '🔧Изменить пароль сервиса🔧')  # Обрабатывает кнопку 🔧Изменить пароль🔧
async def del_service(message: Message, state: FSMContext):
    user = await db.get_value('id', message.from_user.id)
    if await db.user_in_base(message.from_user.id):
        if user[6]:
            await message.answer('Введите пароль ЛК:')
            await state.set_state(EditPassword.password)
        else:
            data = user[4].split('/')
            s = []
            for i in data:
                s.append(i.split(':')[0])
            await message.answer('Выберите сервис:', reply_markup=keyboards.services_edit_keyboard(s))
            await state.clear()
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.text == '🔑Получить пароль сервиса🔑')  # Обрабатывает кнопку 📥Получить пароль📥
async def del_service(message: Message, state: FSMContext):
    user = await db.get_value('id', message.from_user.id)
    if await db.user_in_base(message.from_user.id):
        if user[6]:
            await message.answer('Введите пароль ЛК:')
            await state.set_state(GetPassword.password)
        else:
            data = await db.get_value('id', message.from_user.id)
            data = data[4].split('/')
            s = []
            for i in data:
                s.append(i.split(':')[0])
            await message.answer('Выберите сервис:', reply_markup=keyboards.services_keyboard(s))
            await state.clear()
    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(F.sticker)  # Обрабатывает неизвесный текст
async def other_messages(message: Message):
    await message.bot.send_sticker(message.chat.id,
                                   message.sticker.file_id)


@router.message()  # Обрабатывает неизвесный текст
async def other_messages(message: Message):
    await message.answer('Для навигации используйте кнопки')
