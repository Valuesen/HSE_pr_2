from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    name = State()
    password = State()
    secret_code = State()


class AddServiceStates(StatesGroup):
    service_name = State()
    service_login = State()
    service_password = State()


class EditServiceStates(StatesGroup):
    service_login = State()
    service_password = State()


class EditName(StatesGroup):
    name = State()


class EditPeriod(StatesGroup):
    new_period = State()


class GetPassword(StatesGroup):
    password = State()


class DeleteService(StatesGroup):
    password = State()


class EditPassword(StatesGroup):
    password = State()


class DeleteAccount(StatesGroup):
    password = State()


class EditAccountPassword(StatesGroup):
    password = State()
    new_password = State()


class EditAccountPasswordReq(StatesGroup):
    password = State()
