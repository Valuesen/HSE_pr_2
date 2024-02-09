from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from Texts.texts import MESSAGES

from src.states.user_states import UserStates, AddServiceStates, DeleteService, GetPassword
from src.keyboards import keyboards
from src.services.sql import DataBase
from src.config import database_path


router = Router()
db = DataBase(database_path)  # Подключение базы данных


@router.message(CommandStart())    # Роутер на команду /start
async def start(message: Message, state: FSMContext):
    if await db.user_in_base(message.from_user.id):
        await message.answer('Вы уже зарегестрированы', reply_markup=keyboards.main_menu_keyboard())
    else:
        await message.answer(MESSAGES["start_message"])
        await state.set_state(UserStates.name)


@router.message(Command("help"))    # Роутер на команду /help
async def help_message(message: Message):
    await message.answer(MESSAGES['help'])


@router.message(Command("add_service"))    # Роутер на команду /add_service
async def add_service(message: Message, state: FSMContext):
    await message.answer('Напишите название сервиса\n(Не используйте : и /):', reply_markup=None)
    await state.set_state(AddServiceStates.service_name)


@router.message(Command("del_service"))    # Роутер на команду /del_service
async def del_service(message: Message, state: FSMContext):
    if await db.user_in_base(message.from_user.id):
        user = await db.get_value('id', message.from_user.id)
        if user[6]:
            await message.answer('Введите пароль:')
            await state.set_state(DeleteService.password)
        else:
            data = user[4].split('/')
            s = []
            for i in data:
                s.append(i.split(':')[0])
            await message.answer('Выберите сервис:', reply_markup=keyboards.services_delete_keyboard(s))

    else:
        await message.answer(MESSAGES['user_not_in_base'], reply_markup=keyboards.start_keyboard())


@router.message(Command("get_pwd"))    # Роутер на команду /get_pwd
async def del_service(message: Message, state: FSMContext):
    user = await db.get_value('id', message.from_user.id)
    if await db.user_in_base(message.from_user.id):
        if user[6]:
            await message.answer('Введите пароль:')
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


@router.message(Command("account"))    # Роутер на команду /account
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
