import telebot

bot = telebot.TeleBot('*****')


# Обычный режим
# @bot.message_handler(content_types=["text"])
# def any_msg(message):
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     callback_button = telebot.types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
#     keyboard.add(callback_button)
#     bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)


# Инлайн-режим с непустым запросом
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = telebot.types.InlineKeyboardMarkup()
    # Добавляем колбэк-кнопку с содержимым "test"
    kb.add(telebot.types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = []
    single_msg = telebot.types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=telebot.types.InputTextMessageContent(
            message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Пыщь")
            # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
            #                       text="Пыщь")
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пыщь!")
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")


@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    switch_button = telebot.types.InlineKeyboardButton(text="Нажми меня", switch_inline_query="Telegram")
    keyboard.add(switch_button)
    bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling(none_stop=True)
