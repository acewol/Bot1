import telebot
import config
import random

from telebot import types


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static\welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Маленькая клавиатура
    item1 = types.KeyboardButton("Рандомное число")
    item2 = types.KeyboardButton("Как дела ?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот создан просто так.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела ?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1,item2)

            bot.send_message(message.chat.id, 'Отлично, как сам ?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и хорошо')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Главное не сдавайся и все получится')

            #remove
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Как дела ?",
                reply_markup=None)

            bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False,
                text="Это пробное уведомление !")

    except Exception as e:
        print(repr(e))

# Запуск
bot.polling(none_stop=True)