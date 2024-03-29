import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print('ok')

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
password TEXT NOT NULL,
period INTEGER NOT NULL,
passwords TEXT NOT NULL,
alerts INTEGER NOT NULL,
pwd_req INTEGER NOT NULL
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()