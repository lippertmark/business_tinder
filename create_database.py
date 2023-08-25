from config import *
import mysql.connector
from db_utils import *

try:
    connector = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = connector.cursor()

    query = f'CREATE DATABASE {database};'
    cursor.execute(query)
    cursor.close()
    connector.close()
except mysql.connector.errors.DatabaseError:
    print("Database 'tinder' already exists")




db = DB(host=host, user=user, password=password, database=database)

db.create_db_tg_users()
db.create_db_done_users()


db.close()