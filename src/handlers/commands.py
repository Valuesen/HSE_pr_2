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

