import telebot
from db_utils import *
from telebot import types
from config import *
from keyboards import *

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

db = DB(host=host, user=user, password=password, database=database)


@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    tg_id = message.chat.id
    username = message.chat.username
    if username == None:
        username = 'недоступен'
    user_info = db.get_user(tg_id)
    if user_info == None:
        db.add_user_to_db(tg_id)
        bot.send_message(chat_id=tg_id,
                         text='Добро пожаловать в бота знакомств, '
                              'здесь вы сможете найти полезные знакомства или просто найти нового партнера 🧑‍💼👩‍💼 для бизнеса 💼\n\n'
                              'Для использования бота нужно заполнить анкету 📃. Введи свое ФИО)')
        db.update_user(tg_id=tg_id, fields_with_values={'user_state': 'wait_fio', 'username': username})
    else:
        user_info = db.get_user(tg_id)
        if user_info['user_state'] == 'wait_fio':
            bot.send_message('Вы не закончили заполнение анкеты 😔\n Введите свое ФИО')
        elif user_info['user_state'] == 'wait_age':
            bot.send_message('Вы не закончили заполнение анкеты 😔\n Введите свой возраст')
        elif user_info['user_state'] == 'wait_education':
            bot.send_message('Вы не закончили заполнение анкеты 😔')
            ask_education(tg_id=tg_id)
        elif user_info['user_state'] == 'done':
            bot.send_message(chat_id=tg_id,
                             text='Вы уже заполнили анкету! ✅ Перейдем к просмотру анкет других пользователей? 👀',
                             reply_markup=get_main_keyboard())


def ask_education(tg_id):
    bot.send_message(chat_id=tg_id, text='Выбери свой уровень образования 🏫', reply_markup=get_education_keyboard())


def show_user(tg_id, other_user_tg_id):
    other_user_info = db.get_user(other_user_tg_id)
    bot.send_photo(
        chat_id=tg_id,
        photo=other_user_info['photo_file_id'],
        caption=f'@{other_user_info["username"]}\n'
                f'{other_user_info["fio"]}, {other_user_info["age"]}\n'
                f'Образование: {other_user_info["education"]}',
        reply_markup=get_next_keyboard()
    )


def give_offer(tg_id: int):
    user_info = db.get_user(tg_id=tg_id)
    other_users = db.get_other_users(tg_id=tg_id)
    previous_viewed = user_info['last_viewed']
    if len(other_users) == 0:
        bot.send_message(chat_id=tg_id,
                         text="К сожалению, пока что нет других пользователей, попробуй зайти в бота немного позже ⏳")
    elif previous_viewed == "":
        other_user_id = other_users[0]
        show_user(tg_id, other_user_id)
        db.update_user(tg_id=tg_id, fields_with_values={'last_viewed': str(other_user_id)})
    else:
        other_user_id = other_users[(other_users.index(str(previous_viewed)) + 1) % len(other_users)]
        show_user(tg_id=tg_id, other_user_tg_id=other_user_id)
        db.update_user(tg_id=tg_id, fields_with_values={'last_viewed': str(other_user_id)})


@bot.message_handler(content_types=['text'])
def text_handler(message: types.Message):
    tg_id = message.chat.id
    user_info = db.get_user(tg_id)
    if user_info == None:
        bot.send_message(chat_id=tg_id, text='Напиши команду /start, для активации бота 🧩')
        return
    state = user_info['user_state']
    if message.text == 'Смотреть анкеты 👀':
        give_offer(tg_id)
        return
    if state == 'done':
        bot.send_message(chat_id=tg_id,
                         text='Вы уже заполнили анкету! ✅ Перейдем к просмотру анкет других пользователей? 👀',
                         reply_markup=get_main_keyboard())
        return
    if state == 'wait_fio':
        bot.send_message(chat_id=tg_id, text='Сколько тебе лет?')
        db.update_user(tg_id, {'fio': message.text, 'user_state': 'wait_age'})
        return
    if state == 'wait_age':
        age = message.text
        if age.isdigit():
            photos = bot.get_user_profile_photos(user_id=tg_id).photos
            data = {'age': message.text}
            if len(photos) != 0:
                file_id = photos[0][2].file_id
                data['photo_file_id'] = file_id
                data['user_state'] = 'wait_education'
                ask_education(tg_id=tg_id)
            else:
                bot.send_message(chat_id=tg_id, text='Пришли свое фото для анкеты')
                data['user_state'] = 'wait_photo'
            db.update_user(tg_id, data)
        else:
            bot.send_message(chat_id=tg_id, text='Вы ввели не число, попробуйте еше раз)')


@bot.message_handler(content_types=["photo"])
def photo_handler(message):
    tg_id = message.chat.id
    file_id = message.photo[2].file_id
    db.update_user(tg_id=tg_id, fields_with_values={'photo_file_id': file_id, 'user_state': 'wait_education'})
    ask_education(tg_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    tg_id = call.from_user.id
    user_info = db.get_user(tg_id)
    if user_info is None:
        bot.send_message(chat_id=tg_id, text='Напиши команду /start, для активации бота 🧩')
        return
    if call.data == 'next':
        give_offer(tg_id)
    if call.data in education_options and user_info['user_state'] == 'wait_education':
        db.update_user(tg_id=tg_id, fields_with_values={'user_state': 'done', 'education': call.data})
        db.add_done_user(tg_id)
        bot.send_message(chat_id=tg_id,
                         text='Спасибо за заполнение анкеты, '
                              'теперь можно перейти к просмотру анкет других пользователей! 👀',
                         reply_markup=get_main_keyboard())
        bot.edit_message_reply_markup(chat_id=tg_id, message_id=call.message.id, reply_markup=None)


bot.infinity_polling()

db.close()
