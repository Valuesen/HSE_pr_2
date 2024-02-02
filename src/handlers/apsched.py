import datetime

from aiogram import Bot
from src.services.sql import DataBase
from src.config import database_path

db = DataBase(database_path)

"""
Данная функция отвечает за напоминание о смене пароля
В данный момент она вызывается раз в 24 часа и отправляет всем пользователям сообщение о необходимости смены пароля
В ближайшее время в базе данных будет внесено изменение формата хранения паролей (добавится дата, в которую пароль 
был обновлен)
Функция будет проверять даты обн. каждого отдельного сервиса для кажного отдельного пользователя
"""


async def time_cheking(bot: Bot):
    pass
    #data = await db.get_all()
    #for i in data:
        #time = i[4].split(':')[2].split('-')
        #print(time)
        #print(datetime.date(int(time[0]), int(time[1]), int(time[2])) - datetime.date.today())
        #await bot.send_message(i[0], 'Пора обновить пароли!')
