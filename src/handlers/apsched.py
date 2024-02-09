from datetime import date

from aiogram import Bot
from src.services.sql import DataBase
from src.config import database_path
from src.keyboards.keyboards import apsched_keyboad

db = DataBase(database_path)

"""
Данная функция отвечает за напоминание о смене пароля
В данный момент она вызывается раз в 24 часа и отправляет всем пользователям сообщение о необходимости смены пароля
"""


async def time_cheking(bot: Bot):
    data = await db.get_value('alerts', 1)
    if type(data) is tuple:
        data = [data]
    for user in data:
        services = user[4].split('/')
        period = user[3]
        text = []
        for service in services:
            data_in_serv = service.split(":")
            time = data_in_serv[2].split('-')
            k = str(date(int(time[0]), int(time[1]), int(time[2])) - date.today())
            if k == '0:00:00':
                pass
            else:
                k = int(k.split(' ')[0])
                if period + k <= 0:
                    text.append(data_in_serv[0])
        if text:
            await bot.send_message(user[0], 'Пора обновить пароли в этих сервисах!\nСписок:\n' + '\n'.join(text),
                                   reply_markup=apsched_keyboad())
