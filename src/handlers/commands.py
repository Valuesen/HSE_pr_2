from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router

from Texts.texts import MESSAGES

from src.states.user_states import UserStates
from src.keyboards.keyboards import main_menu_keyboard
from src.services.sql import DataBase
from src.config import database_path

router = Router()
database = DataBase(database_path)  # Подключение базы данных


@router.message(CommandStart())    # Роутер на команду /start
async def start(message: Message, state: FSMContext):
    if await database.user_in_base(message.from_user.id):
        await message.answer('Вы уже зарегестрированы', reply_markup=main_menu_keyboard())
        print(message.from_user.username)
    else:
        await message.answer(MESSAGES["start_message"])
        await state.set_state(UserStates.name)
