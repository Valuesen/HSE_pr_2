import sqlite3


class DataBase:
    def __init__(self, db_path):
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()

    async def update_passwords(self, user_id, value):
        with self.connect:
            try:
                sql_update_query = f"""Update Users set passwords = '{str(value)}' where id = {user_id}"""
                return self.cursor.execute(sql_update_query)
            except sqlite3.Error as e:
                print(e)

    async def update_name(self, user_id, value):
        with self.connect:
            try:
                sql_update_query = f"""Update Users set name = '{str(value)}' where id = {user_id}"""
                return self.cursor.execute(sql_update_query)
            except sqlite3.Error as e:
                print(e)

    async def update_peroid(self, user_id, value):
        with self.connect:
            try:
                sql_update_query = f"""Update Users set period = '{int(value)}' where id = {user_id}"""
                return self.cursor.execute(sql_update_query)
            except sqlite3.Error as e:
                print(e)

    async def get_value(self, selection, value):
        try:
            with self.connect:
                data = self.cursor.execute(f"SELECT * FROM Users WHERE {selection} = {value}")
                for row in data:
                    i = row
            try:
                return i
            except Exception as e:
                print(e)
                return 0
        except sqlite3.Error as error:
            print(error)

    async def get_all(self):
        with self.connect:
            i = []
            data = self.cursor.execute(f"SELECT * FROM Users")
            for row in data:
                i.append(row)
        try:
            return i
        except Exception as e:
            print(e)
            return 0

    async def add_user(self, user):
        with self.connect:
            return self.cursor.execute(
                f'INSERT INTO Users (id, name, password, period, passwords) values{tuple(user)}')

    async def delete(self, selection, value):
        with self.connect:
            sql_delete_query = f"""DELETE from Users where {selection} = {value}"""
            return self.cursor.execute(sql_delete_query)

    async def user_in_base(self, user_id):
        with self.connect:
            i = []
            data = self.cursor.execute(f"SELECT id FROM Users")
            for row in data:
                i.append(int(str(row).replace('(', '').replace(',)', '')))
            return user_id in i
