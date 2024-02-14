import datetime
import random
from src.services.pwd_cheking import pwd_check

chars = '+-*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


async def get_delta_time(user, today_data, service=''):
    services = user[4].split('/')
    print(service)
    text = []
    if service == '':
        for i in services:
            data_in_serv = i.split(":")
            time = data_in_serv[3].split('-')
            k = str(datetime.date(int(time[0]), int(time[1]), int(time[2])) - today_data)
            if k == '0:00:00':
                text.append(f"{data_in_serv[0]}: {user[3]} дн. до смены пароля")
            else:
                k = int(k.split(' ')[0])
                if user[3] + k > 0:
                    text.append(f"{data_in_serv[0]}: {user[3] + k} дн. до смены пароля")
                else:
                    text.append(f"{data_in_serv[0]}: пора менять")
        return text
    else:
        for i in services:
            if i.split(':')[0] == service:
                data_in_serv = i.split(":")
                time = data_in_serv[3].split('-')
                k = str(datetime.date(int(time[0]), int(time[1]), int(time[2])) - today_data)
                if k == '0:00:00':
                    return str(user[3]) + ' дн.'
                else:
                    k = int(k.split(' ')[0])
                    if user[3] + k > 0:
                        return str(user[3] + k) + ' дн.'
                    else:
                        return 'Пора менять'


async def generate_pwd():
    while 1:
        password = ''
        for i in range(11):
            password += random.choice(chars)
        if await pwd_check(password) == 'отличый🟢':
            break
    return password
