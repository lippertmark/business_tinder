import logging

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w")
logging.getLogger('mysql.connector').disabled =True
logging.getLogger('urllib3.connectionpool').disabled = True

host = 'localhost'
user = 'root'
password = '1234-qwer'
database = 'tinder'

TELEGRAM_TOKEN = '6538137681:AAEUIRAyv8SD_2xFUxwnlNyrZ9Jwq0COnes'