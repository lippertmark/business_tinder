from telebot import types

education_options = ['Школа 🎒', 'Бакалавриат 🏫', 'Магистратура 👨‍🎓', 'Аспирантура 👨‍🔬']

def get_education_keyboard():
    education_keyboard = types.InlineKeyboardMarkup()
    for item in education_options:
        education_keyboard.add(types.InlineKeyboardButton(item, callback_data=item))
    return education_keyboard

def get_next_keyboard():
    next_keyboard = types.InlineKeyboardMarkup()
    next_keyboard.add(types.InlineKeyboardButton('Следующая анкета', callback_data='next'))
    return next_keyboard

def get_main_keyboard():
    main_keyboard = types.ReplyKeyboardMarkup()
    main_keyboard.add(types.KeyboardButton('Смотреть анкеты 👀'))
    return main_keyboard