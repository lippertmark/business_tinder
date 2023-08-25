import mysql.connector
from config import *


tg_users_attributes = ['tg_id', 'fio', 'username', 'photo_file_id', 'age', 'education', 'user_state', 'last_viewed']


class DB:
    def __init__(self, host, user, password, database):
        self.connector = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connector.cursor()


    def create_db_tg_users(self):
        query = 'CREATE TABLE tg_users (' \
                'tg_id varchar(255) DEFAULT "",' \
                'fio varchar(255) DEFAULT "",' \
                'username varchar(255) DEFAULT "",' \
                'photo_file_id varchar(255) DEFAULT "",' \
                'age int DEFAULT NULL,' \
                'education varchar(255) DEFAULT "",' \
                'user_state varchar(255) DEFAULT "start",' \
                'last_viewed varchar(255) DEFAULT ""' \
                ');'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')


    def create_db_done_users(self):
        query = 'CREATE TABLE done_users (' \
                'tg_id varchar(255) DEFAULT ""' \
                ');'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')

    def delete_table_tg_users(self):
        query = 'DROP TABLE tg_users;'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')

    def delete_table_done_users(self):
        query = 'DROP TABLE done_users;'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')

    def add_done_user(self, tg_id: int):
        query = f'INSERT INTO done_users(tg_id) VALUES("{tg_id}")'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')
        self.connector.commit()





    def add_user_to_db(self, tg_id: int):
        query = f'INSERT INTO tg_users(tg_id) VALUES("{tg_id}")'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')
        self.connector.commit()


    def get_user(self, tg_id: int):
        query = f'SELECT * FROM tg_users WHERE tg_id = "{tg_id}"'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None
        else:
            return dict(zip(tg_users_attributes, data[0]))


    def set_state(self, tg_id: int, user_state: str):
        query = f'UPDATE tg_users SET user_state = "{user_state}" WHERE tg_id = "{tg_id}"'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')
        self.connector.commit()

    @staticmethod
    def dict_to_query(fields_with_values: dict):
        columns = []
        if 'tg_id' in fields_with_values:
            fields_with_values['tg_id'] = str(fields_with_values['tg_id'])
        for field, value in fields_with_values.items():
            column = f'{field} = '
            if isinstance(value, int):
                column += f'{value}'
            elif isinstance(value, str):
                column += f'"{value}"'
            columns.append(column)
        response = ', '.join(columns)
        return response


    def update_user(self, tg_id: int, fields_with_values: dict):
        query = f'UPDATE tg_users SET {DB.dict_to_query(fields_with_values)} WHERE tg_id = "{tg_id}"'
        self.cursor.execute(query)
        logging.info(f'SQL: {query}')
        self.connector.commit()


    def get_other_users(self, tg_id: int):
        query = f'SELECT * FROM done_users WHERE (tg_id != "{tg_id}")'
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        data = list(map(lambda x: x[0], data))
        return data

    def close(self):
        self.cursor.close()
        self.connector.close()

# delete_table_tg_users()
# create_db_tg_users()
# create_db_done_users()
# add_done_user(338600505)
# add_done_user(679352808)
# add_done_user(1284017375)
# add_user_to_db(123)
# print(get_user(123))
# update_user(tg_id=123, fields_with_values={'username': 'lippertmark', 'age': 15})
# print(get_other_users(338600505))
# print(get_other_users(338600505))
