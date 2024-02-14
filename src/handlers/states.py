"""
В данном файле происходит обработка измененией состояний
"""

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

import asyncio

from Texts.texts import MESSAGES
from src.states import user_states
from src.keyboards import keyboards
from src.services.sql import DataBase
from src.config import database_path
from src.states.user_states import EditAccountPasswordReq

from src.services.pwd_cheking import pwd_check
from src.services.spec_func import generate_pwd

router = Router()
database = DataBase(database_path)


@router.message(user_states.UserStates.name)
async def start_pass(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(user_name=message.text)
        await message.answer(f'Прияно познакомиться, {message.text}!\n'
                             f'Создайте пароль для вашего личного кабинета:')
        await state.set_state(user_states.UserStates.password)
    else:
        await message.answer('Неверный формат ввода, пожалуйста, введите имя текстом')
        await state.set_state(user_states.UserStates.name)


@router.message(user_states.EditPeriod.new_period)
async def start_pass(message: Message, state: FSMContext):
    try:
        new_period = int(message.text)
        await database.update_peroid(message.from_user.id, new_period)
        user = await database.get_value('id', message.from_user.id)
        m = await message.answer('Готово 🚀')
        await asyncio.sleep(2)
        await m.delete()
        await asyncio.sleep(0.2)
        await message.answer(
            f'Имя: {user[1]}\nСервисов добавлено: {len(user[4].split("/"))}\nПериод: {user[3]} д.\n'
            f'Уведомления: {"Включены🟢" if user[5] == 1 else "Выключены🔴"}\n'
            f'Запрос пароля: {"Включен🟢" if user[6] == 1 else "Выключен🔴"}',
            reply_markup=keyboards.edit_account_keyboard(user))
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer(f'Ошибка изменения периода\nИспользуйте только цивры!\nНапишите период:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.EditPeriod.new_period)


@router.message(user_states.UserStates.password)
async def start_sec(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(pwd_message=message.text)
        await message.answer(MESSAGES["final_reg"], reply_markup=keyboards.main_menu_keyboard())
        data = await state.get_data()
        await database.add_user([message.from_user.id, data['user_name'], data["pwd_message"], 60, '', 1, 1])
        await state.clear()
    else:
        await message.answer('Неверный формат ввода, пожалуйста, введите текстовый пароль',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.UserStates.password)


@router.message(user_states.AddServiceStates.service_name)
async def add_serv_name(message: Message, state: FSMContext):
    if message.text:
        if message.text in ['📋Список моих сервисов📋', '✅Добавить✅', '❌Удалить❌', '⬅Главное меню']:
            await message.answer('Добавление приостановлено,\nначните заново')
            await state.clear()
        else:
            await state.update_data(service_name=message.text.replace(':', '').replace('/', ''))
            await state.set_state(user_states.AddServiceStates.service_login)
            await message.answer('Введите логин для данного сервиса\n'
                                 'Не используйте / и :', reply_markup=keyboards.pass_keyboard())

    else:
        await message.answer('Ошибка ввода\nПришлите текстовое название сервиса:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.AddServiceStates.service_name)


@router.message(user_states.AddServiceStates.service_login)
async def add_serv_log(message: Message, state: FSMContext):
    if message.text:
        if message.text in ['📋Список моих сервисов📋', '✅Добавить✅', '❌Удалить❌', '⬅Главное меню']:
            await message.answer('Добавление приостановлено,\nначните заново')
            await state.clear()
        else:
            if message.text == '🔽Пропустить🔽':
                await state.update_data(service_login='Не указан')
            else:
                await state.update_data(service_login=message.text.replace(':', '').replace('/', ''))
            await state.set_state(user_states.AddServiceStates.service_password)
            await message.answer('Введите пароль к данному сервису\n'
                                 'Не используйте / и :', reply_markup=keyboards.random_gen_keyboard())

    else:
        await message.answer('Ошибка ввода\nПришлите текстовое название сервиса:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.AddServiceStates.service_login)


@router.message(user_states.AddServiceStates.service_password)
async def add_serv_pwd(message: Message, state: FSMContext):
    if message.text:

        if message.text == '🎲Генирация пароля🎲':
            await state.update_data(service_password=await generate_pwd())
        else:
            await state.update_data(service_password=message.text.replace(':', '').replace('/', ''))
        data = await state.get_data()

        sec = await pwd_check(data['service_password'])
        await message.answer(f'Сервис: {data["service_name"]}\n'
                             f'Логин: {data["service_login"]}\n'
                             f'Пароль: {data["service_password"]}\n'
                             f'Пароль {sec}',
                             reply_markup=keyboards.verification_keyboard('add'))
    else:
        await message.answer('Неверный формат ввода, введите пароль текстом:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.AddServiceStates.service_password)


@router.message(user_states.EditServiceStates.service_password)
async def add_serv_name(message: Message, state: FSMContext):
    if message.text:
        if message.text == '🎲Генирация пароля🎲':
            await state.update_data(service_password=await generate_pwd())
        else:
            await state.update_data(service_password=message.text.replace(':', '').replace('/', ''))

        data = await state.get_data()
        sec = await pwd_check(data['service_password'])
        await message.answer(f'Сервис: {data["service_name"]}\n'
                             f'Пароль: {data["service_password"]}\n'
                             f'Пароль {sec}',
                             reply_markup=keyboards.verification_keyboard(data["func"]))
    else:
        await message.answer('Неверный формат ввода, введите пароль текстом:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.EditServiceStates.service_password)


@router.message(user_states.EditServiceStates.service_login)
async def add_serv_name(message: Message, state: FSMContext):
    if message.text:
        if message.text == '🔽Пропустить🔽':
            await state.update_data(service_login='Не указан')

        else:
            await state.update_data(service_login=message.text.replace(':', '').replace('/', ''))

        data = await state.get_data()
        await message.answer(f'Сервис: {data["service_name"]}\n'
                             f'Логин: {data["service_login"]}',
                             reply_markup=keyboards.verification_keyboard(data["func"]))
    else:
        await message.answer('Неверный формат ввода, введите пароль текстом:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.EditServiceStates.service_password)


@router.message(user_states.EditName.name)
async def edit_name(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(user_name=message.text)
        await message.answer(f'Новое имя: {message.text}',
                             reply_markup=keyboards.verification_keyboard('edit_name'))
    else:
        await message.answer('Неверный формат ввода\nВведите имя текстом:')
        await state.set_state(user_states.EditName.name)


@router.message(user_states.GetPassword.password)
async def get_pwd(message: Message, state: FSMContext):
    user = await database.get_value('id', message.from_user.id)
    if message.text:
        if message.text == user[2]:
            try:
                lm = await state.get_data()
                lm = lm['last_message']
                await lm.delete()
            except Exception as e:
                print(e)
            data = user[4].split('/')
            s = []
            for i in data:
                s.append(i.split(':')[0])
            if s == ['']:
                await message.answer('Нет доступных сервисов\nДобавите их, используя кнопку ✅Добавить✅')
            else:
                await message.answer('Выберите сервис:', reply_markup=keyboards.services_main_keyboard(s))
            await state.clear()
        else:
            try:
                lm = await state.get_data()
                lm = lm['last_message']
                await lm.delete()
            except Exception as e:
                print(e)
            last_message = await message.answer('Неверный пароль\nВведите пароль заново:',
                                                reply_markup=keyboards.cancel_keyboard())
            await state.update_data(last_message=last_message)
            await state.set_state(user_states.GetPassword.password)
    else:
        await message.answer('Ошибка входа')
        await state.clear()


@router.message(user_states.DeleteService.password)
async def del_service(message: Message, state: FSMContext):
    user = await database.get_value('id', message.from_user.id)
    if user[6]:
        if message.text:
            if message.text == user[2]:
                try:
                    lm = await state.get_data()
                    lm = lm['last_message']
                    await lm.delete()
                except Exception as e:
                    print(e)
                data = user[4].split('/')
                s = []
                for i in data:
                    s.append(i.split(':')[0])
                if s == ['']:
                    await message.answer('Нет доступных сервисов\nДобавите их, используя кнопку ✅Добавить✅')
                else:
                    await message.answer('Выберите сервис:', reply_markup=keyboards.services_main_keyboard(s))
                await state.clear()
            else:
                try:
                    lm = await state.get_data()
                    lm = lm['last_message']
                    await lm.delete()
                except Exception as e:
                    print(e)
                last_message = await message.answer('Неверный пароль\nВведите пароль заново:',
                                                    reply_markup=keyboards.cancel_keyboard())
                await state.update_data(last_message=last_message)
                await state.set_state(user_states.DeleteService.password)
        else:
            await message.answer('Ошибка входа\n')
            await state.clear()
    else:
        data = user[4].split('/')
        s = []
        for i in data:
            s.append(i.split(':')[0])
        await message.answer('Выберите сервис:', reply_markup=keyboards.services_delete_keyboard(s))
        await state.clear()


@router.message(user_states.DeleteAccount.password)
async def del_account(message: Message, state: FSMContext):
    user = await database.get_value('id', message.from_user.id)
    if message.text:
        if message.text == user[2]:
            await message.answer('Вы уверены, что хотите удалить аккаунт без возможности восстаноления?',
                                 reply_markup=keyboards.verification_keyboard('del_account'))
        else:
            await message.answer('Ошибка входа', reply_markup=keyboards.main_menu_keyboard())
        await state.clear()
    else:
        await message.answer('Ошибка ввода\nВведите текстовый пароль:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.DeleteAccount.password)


@router.message(EditAccountPasswordReq.password)  # Роутер на изменение параметров аккаунта
async def edit_account_password_req(message: Message, state: FSMContext):
    user = await database.get_value('id', message.from_user.id)
    if message.text:
        if message.text == user[2]:
            if user[6] == 1:
                await database.update_pwd_req(message.from_user.id, 0)
            else:
                await database.update_pwd_req(message.from_user.id, 1)
            user = await database.get_value('id', message.from_user.id)
            x = user[4].split("/")
            await message.answer(
                f'Имя: {user[1]}\nСервисов добавлено: {0 if x == [""] else len(x)}\nПериод: {user[3]} д.\n'
                f'Уведомления: {"Включены🟢" if user[5] == 1 else "Выключены🔴"}\n'
                f'Запрос пароля: {"Включен🟢" if user[6] == 1 else "Выключен🔴"}',
                reply_markup=keyboards.edit_account_keyboard(user))
        else:
            x = user[4].split("/")
            last = await message.answer('❌Пароль неверен❌')
            await asyncio.sleep(1)
            await last.edit_text(
                f'Имя: {user[1]}\nСервисов добавлено: {0 if x == [""] else len(x)}\nПериод: {user[3]} д.\n'
                f'Уведомления: {"Включены🟢" if user[5] == 1 else "Выключены🔴"}\n'
                f'Запрос пароля: {"Включен🟢" if user[6] == 1 else "Выключен🔴"}',
                reply_markup=keyboards.edit_account_keyboard(user))
        await state.clear()
    else:
        await message.answer('Ошибка ввода\nВведите текстовый пароль:', reply_markup=keyboards.cancel_keyboard())
        await state.set_state(EditAccountPasswordReq.password)


@router.message(user_states.EditAccountPassword.password)
async def edit_pwd(message: Message, state: FSMContext):
    user = await database.get_value('id', message.from_user.id)
    if message.text:
        if message.text == user[2]:
            await message.answer('Введите новый пароль:')
            await state.set_state(user_states.EditAccountPassword.new_password)
        else:
            await message.answer('Ошибка входа', reply_markup=keyboards.main_menu_keyboard())
            await state.clear()
    else:
        await message.answer('Ошибка ввода\nВведите текстовый пароль:', reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.EditAccountPassword.password)


@router.message(user_states.EditAccountPassword.new_password)
async def edit_pwd(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(new_account_password=message.text)
        await state.set_state(user_states.EditAccountPassword.new_password)
        await message.answer(f'Вы уверены, что хотите сменить пароль на {message.text}?',
                             reply_markup=keyboards.verification_keyboard('edit_ac_pwd'))
    else:
        await message.answer('Неверный формат ввода,\nНапишите текстовый пароль:',
                             reply_markup=keyboards.cancel_keyboard())
        await state.set_state(user_states.EditAccountPassword.new_password)
