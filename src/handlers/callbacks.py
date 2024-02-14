from aiogram.types import CallbackQuery
from aiogram import F
from aiogram import Router
import asyncio
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from src.services.sql import DataBase
from src.services.spec_func import get_delta_time
from src.config import database_path
from src.keyboards import keyboards
from src.states.user_states import (EditServiceStates, EditName, EditPeriod, DeleteAccount, EditAccountPassword,
                                    EditAccountPasswordReq)

from datetime import date

from Texts.texts import MESSAGES

db = DataBase(database_path)
router = Router()


@router.callback_query(F.data == 'close_profile_menu')  # Роутер на закрытие меню аккаунта
async def close_profile_menu(callback: CallbackQuery):
    await callback.message.edit_text("❌Закрыто❌",
                                     reply_markup=None)
    await asyncio.sleep(3)
    await callback.message.delete()


@router.callback_query(F.data == 'edit_profile')  # Роутер на изменение параметров аккаунта
async def edit_menu(callback: CallbackQuery):
    user = await db.get_value('id', callback.from_user.id)
    await callback.message.edit_text(
        f'Имя: {user[1]}\n'
        f'Запрос пароля ЛК: {"Вкл.🟢" if user[6] == 1 else "Выкл.🔴"}\n'
        f'Уведомления: {"Вкл.🟢" if user[5] == 1 else "Выкл.🔴"}\n'
        f'Смена пароля: каждые {user[3]} дн.\n'
        f'Сервисов добавлено: {0 if user[4].split("/") == [""] else len(user[4].split("/"))}\n',
        reply_markup=keyboards.edit_account_keyboard(user))


@router.callback_query(F.data == 'edit_alerts')  # Роутер на изменение параметров аккаунта
async def edit_alerts(callback: CallbackQuery):
    user = await db.get_value('id', callback.from_user.id)
    if user[5] == 1:
        await db.update_alerts(callback.from_user.id, 0)
    else:
        await db.update_alerts(callback.from_user.id, 1)
    user = await db.get_value('id', callback.from_user.id)
    x = user[4].split("/")
    await callback.message.edit_text(
        f'Имя: {user[1]}\n'
        f'Запрос пароля ЛК: {"Вкл.🟢" if user[6] == 1 else "Выкл.🔴"}\n'
        f'Уведомления: {"Вкл.🟢" if user[5] == 1 else "Выкл.🔴"}\n'
        f'Смена пароля: каждые {user[3]} дн.\n'
        f'Сервисов добавлено: {0 if user[4].split("/") == [""] else len(user[4].split("/"))}\n',
        reply_markup=keyboards.edit_account_keyboard(user))


@router.callback_query(F.data == 'cancel')  # Роутер на кноаку Отемна(Во всех функциях)
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer('❌Отмена❌', reply_markup=keyboards.pwd_menage_keyboard())


@router.callback_query(F.data == 'close')  # Роутер на кнопку Закрыть(Во всех функциях)
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌Закрыто❌")


@router.callback_query(F.data == 'add_service')  # Роутер на добавление сервиса
async def add_service(callback: CallbackQuery, state: FSMContext):
    last_data = await db.get_value('id', callback.from_user.id)
    data = await state.get_data()
    await state.clear()
    service = data['service_name']
    login = data["service_login"]
    pasword = data['service_password']
    current_date = date.today()
    data = f'{service}:{login}:{pasword}:{current_date}'
    if last_data[4] == '':
        await db.update_passwords(callback.from_user.id, '/'.join([data]))
    else:
        await db.update_passwords(callback.from_user.id, '/'.join([last_data[4], data]))
    await callback.message.edit_text('Сервис добавлен!', reply_markup=None)
    await callback.message.answer('Меню управления сервисами:', reply_markup=keyboards.pwd_menage_keyboard())


@router.callback_query(F.data == 'delete_service')  # Роутер на удаление сервиса
async def delete_service(callback: CallbackQuery, state: FSMContext):
    data_db = await db.get_value('id', callback.from_user.id)
    data_db = data_db[4].split('/')
    data_tg = await state.get_data()
    service = data_tg['service_name']
    for i in data_db:
        if service == i.split(':')[0]:
            data_db.remove(i)
            await db.update_passwords(callback.from_user.id, "/".join(data_db))
            break
    await callback.message.edit_text('Сервис удален!', reply_markup=None)
    await callback.message.answer('Меню управления сервисами:', reply_markup=keyboards.pwd_menage_keyboard())


@router.callback_query(F.data == 'edit_passwd_req')  # Роутер на изменение параметров аккаунта
async def edit_alerts(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите пароль:', reply_markup=None)
    await state.set_state(EditAccountPasswordReq.password)


@router.callback_query(F.data == 'edit_service_password')
async def del_service(callback: CallbackQuery):
    if await db.user_in_base(callback.from_user.id):
        data = callback.message.text.split('\n')[2:]
        s = []
        for i in data:
            s.append(i)
        await callback.message.edit_text('Выберите сервис:', reply_markup=keyboards.services_edit_keyboard(s))
    else:
        await callback.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.callback_query(F.data == 'edit_service')  # Роутер на изменение пароля
async def edit_service(callback: CallbackQuery, state: FSMContext):
    data_db = await db.get_value('id', callback.from_user.id)
    data_db = data_db[4].split('/')
    data_tg = await state.get_data()
    service = data_tg['service_name']
    for i in data_db:
        if service == i.split(':')[0]:
            data = f'{service}:{i.split(":")[1]}:{data_tg["service_password"]}:{date.today()}'
            data_db.remove(i)
            data_db.append(data)
            await db.update_passwords(callback.from_user.id, "/".join(data_db))
            break
    await callback.message.edit_text('Пароль обновлен!', reply_markup=None)
    await state.clear()
    await callback.message.answer('Меню управления сервисами:', reply_markup=keyboards.pwd_menage_keyboard())


@router.callback_query(F.data == 'edit_login_true')  # Роутер на изменение пароля
async def edit_service(callback: CallbackQuery, state: FSMContext):
    data_db = await db.get_value('id', callback.from_user.id)
    data_db = data_db[4].split('/')
    data_tg = await state.get_data()
    service = data_tg['service_name']
    for i in data_db:
        if service == i.split(':')[0]:
            data = f'{data_tg["service_name"]}:{data_tg["service_login"]}:{i.split(":")[2]}:{date.today()}'
            data_db.remove(i)
            data_db.append(data)
            await db.update_passwords(callback.from_user.id, "/".join(data_db))
            break
    await callback.message.edit_text('Логин обновлен!', reply_markup=None)
    await state.clear()
    await callback.message.answer('Меню управления сервисами:', reply_markup=keyboards.pwd_menage_keyboard())


@router.callback_query(F.data == 'edit_period')  # Роутер на изменение пароля
async def edit_name(callback: CallbackQuery, state: FSMContext):
    last_period = await db.get_value('id', callback.from_user.id)
    await callback.message.edit_text(f'Текущая переодичность: {last_period[3]} дн.\n'
                                     f'Задайте новую(в днях):')
    await state.set_state(EditPeriod.new_period)


@router.callback_query(F.data == 'edit_name')  # Роутер на изменение пароля
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Напишите новое имя:')
    await state.set_state(EditName.name)


@router.callback_query(F.data == 'edit_name_final')  # Роутер на изменение пароля
async def edit_name_final(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await db.update_name(callback.from_user.id, data['user_name'])
    user = await db.get_value('id', callback.from_user.id)
    await state.clear()
    await callback.message.answer(
        f'Имя: {user[1]}\n'
        f'Запрос пароля ЛК: {"Вкл.🟢" if user[6] == 1 else "Выкл.🔴"}\n'
        f'Уведомления: {"Вкл.🟢" if user[5] == 1 else "Выкл.🔴"}\n'
        f'Смена пароля: каждые {user[3]} дн.\n'
        f'Сервисов добавлено: {0 if user[4].split("/") == [""] else len(user[4].split("/"))}\n',
        reply_markup=keyboards.edit_account_keyboard(user))


@router.callback_query(F.data == 'del_account')  # Роутер на изменение пароля
async def del_account(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите пароль:', reply_markup=None)
    await state.set_state(DeleteAccount.password)


@router.callback_query(F.data == 'edit_passwd')  # Роутер на изменение пароля
async def edit_account_password(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите старый пароль:', reply_markup=None)
    await state.set_state(EditAccountPassword.password)


@router.callback_query(F.data == 'del_account_final')  # Роутер на изменение пароля
async def del_account_final(callback: CallbackQuery, state: FSMContext):
    await db.delete('id', callback.from_user.id)
    await callback.message.edit_text('Ваш аккунт удален', reply_markup=None)
    await state.clear()


@router.callback_query(F.data == 'services_keyboard')  # Роутер на изменение пароля
async def services_keyboard(callback: CallbackQuery):
    data = await db.get_value('id', callback.from_user.id)
    data = data[4].split('/')
    s = []
    for i in data:
        s.append(i.split(':')[0])
    await callback.message.edit_text('Сервисы:', reply_markup=keyboards.services_main_keyboard(s))


@router.callback_query(F.data == 'edit_ac_true')  # Роутер на изменение пароля
async def del_account_final(callback: CallbackQuery, state: FSMContext):
    pwd = await state.get_data()
    await db.update_password(callback.from_user.id, pwd['new_account_password'])
    user = await db.get_value('id', callback.from_user.id)
    await callback.message.edit_text('✅Пароль изменен✅')
    await asyncio.sleep(1)
    await callback.message.edit_text(
        f'Имя: {user[1]}\n'
        f'Запрос пароля ЛК: {"Вкл.🟢" if user[6] == 1 else "Выкл.🔴"}\n'
        f'Уведомления: {"Вкл.🟢" if user[5] == 1 else "Выкл.🔴"}\n'
        f'Смена пароля: каждые {user[3]} дн.\n'
        f'Сервисов добавлено: {0 if user[4].split("/") == [""] else len(user[4].split("/"))}\n',
        reply_markup=keyboards.edit_account_keyboard(user))
    await state.clear()


@router.callback_query()  # Роутер на все динамические колбэки
async def other(callback: CallbackQuery, state: FSMContext):
    if 'service' == callback.data.split(':')[0]:
        data = await db.get_value('id', callback.from_user.id)
        service = callback.data.split(':')[1]
        password = ''
        login = ''
        time = await get_delta_time(data, date.today(), service)
        for i in data[4].split('/'):
            if service == i.split(':')[0]:
                password = i.split(':')[2]
                login = i.split(':')[1]
                break
        await callback.message.edit_text(f'Сервис: {service}\n'
                                         f'Логин: {login}\n'
                                         f'Пароль: <tg-spoiler>{password}</tg-spoiler>\n'
                                         f'До смены пароля: {time}',
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=keyboards.service_keyboard(service))

    elif 'del' == callback.data.split(':')[0]:
        await state.update_data(service_name=callback.data.split(':')[1])
        await callback.message.edit_text(f'Вы уверены, что хотите удалить {callback.data.split(":")[1]}',
                                         reply_markup=keyboards.verification_keyboard('delete'))
    elif 'change_password' == callback.data.split(':')[0]:
        await state.update_data(service_name=callback.data.split(':')[1], func='edit')
        await callback.message.delete()
        await callback.message.answer(f'Напишите новый пароль:', reply_markup=keyboards.random_gen_keyboard())
        await state.set_state(EditServiceStates.service_password)
    elif 'change_login' == callback.data.split(':')[0]:
        await state.update_data(service_name=callback.data.split(':')[1], func='edit_login')
        await callback.message.delete()
        await callback.message.answer(f'Напишите новый логин:', reply_markup=keyboards.pass_keyboard())
        await state.set_state(EditServiceStates.service_login)
