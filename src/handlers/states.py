"""
В данном файле происходит обработка изменение состояний
"""

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from Texts.texts import MESSAGES
from src.states.user_states import UserStates, AddServiceStates, EditServiceStates, EditName
from src.keyboards.keyboards import main_menu_keyboard, verification_keyboard
from src.services.sql import DataBase
from src.config import database_path

router = Router()
database = DataBase(database_path)


# @router.message(UserStates.name)
# async def start_pass(message: Message, state: FSMContext):
#    await state.update_data(name=message.text)
#    await message.answer(MESSAGES["pwd_message"])
#    await state.set_state(UserStates.password)


# @router.message(UserStates.password)
# async def start_sec(message: Message, state: FSMContext):
#    await state.update_data(pwd_message=message.text)
#    await message.answer(MESSAGES['secret_code'])
#    await state.set_state(UserStates.secret_code)


@router.message(UserStates.name)
async def start_fin(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(MESSAGES["final_reg"], reply_markup=main_menu_keyboard())
    data = await state.get_data()
    await database.add_user([message.from_user.id, data['user_name'], '', '', ''])
    await state.clear()


@router.message(AddServiceStates.service_name)
async def add_serv_name(message: Message, state: FSMContext):
    await state.update_data(service_name=message.text.replace(':', '').replace('/', ''))
    await message.answer('Напишите пароль\n(Не используйте : и /):')
    await state.set_state(AddServiceStates.service_password)



@router.message(AddServiceStates.service_password)
async def add_serv_name(message: Message, state: FSMContext):
    await state.update_data(func='add')
    await state.update_data(service_password=message.text.replace(':', '').replace('/', ''))
    data = await state.get_data()
    await message.answer(f'Сервис: {data["service_name"]}\n'
                         f'Пароль: {data["service_password"]}',
                         reply_markup=verification_keyboard(data["func"]))


@router.message(EditServiceStates.service_name)
async def add_serv_name(message: Message, state: FSMContext):
    await state.update_data(service_password=message.text)
    data = await state.get_data()
    await message.answer(f'Сервис: {data["service_name"]}\n'
                         f'Пароль: {data["service_password"]}',
                         reply_markup=verification_keyboard(data["func"]))


@router.message(EditName.name)
async def edit_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(f'Новое имя: {message.text}', reply_markup=verification_keyboard('edit_name'))
