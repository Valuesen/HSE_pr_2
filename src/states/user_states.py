from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    name = State()
    password = State()
    secret_code = State()


class AddServiceStates(StatesGroup):
    service_name = State()
    service_password = State()


class EditServiceStates(StatesGroup):
    service_name = State()


class EditName(StatesGroup):
    name = State()

