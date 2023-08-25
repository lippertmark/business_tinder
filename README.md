# business_tinder - тестовое задание в бизнесс клуб 💼
Бот для знакомств предпринимателей с партнерами и другими людьми 😜
Язык программированияL:  Python 🐍
База данных: MySQL ⚾
Библиотека телеграм: PyTelegramBotApi(telebot)



# Файлы

- create_database.py - создает базу данных, и нужные таблицы
- keyboards.py - создает Inline и Reply клавиатры телеграм
- main.py - главный файл для запуска бота
- config.py - настройки
- db_utils.py - утилиты для работы с базой данных
- requirements.txt - список необходимых библиотек, для работы бота


# Запуск

### Запуск базы данных
```
sudo systemctl start mysql
```
### Установка нужных библиотек
```
pip install -r requirements.txt
```
### Инициализация базы данных и таблиц
```
python3 create_database.py
```
### Запуск бота
```
python3 main.py
```


