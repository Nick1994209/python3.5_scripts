import os
import telebot
import time
from random import shuffle

from botan import botan_tracking
import settings


bot = telebot.TeleBot(settings.BOT_KEY)


# handlers
@bot.message_handler(commands=['start', 'help', 'go'])
def start_handler(message):
    chat_id = message.chat.id
    print(chat_id)
    msg = bot.send_message(chat_id, 'Откуда парсить?')
    bot.register_next_step_handler(msg, next_step)


def next_step(message):
    chat_id = message.chat.id
    print(chat_id, 'next step')
    msg = bot.send_message(chat_id, 'А я есть второй')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    print('repeat_all_messages')
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['test'])
@botan_tracking
def find_file_ids(message):
    bot.send_message(message.chat.id, 'test')

    for file in os.listdir('music/'):
        print()
        if file.split('.')[-1] == 'ogg':
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.chat.id, f, None)
            # А теперь отправим вслед за файлом его file_id
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['key'])
@botan_tracking
def find_file_ids(message):
    bot.send_message(message.chat.id, 'hello', reply_markup=generate_markup('first', 'second'))


def generate_markup(*items):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    shuffle(items)
    for item in items:
        markup.add(item)
    return markup


if __name__ == '__main__':
    bot.polling(none_stop=True)
