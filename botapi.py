import config
import telebot
import random
bot = telebot.TeleBot(config.token)

DIC = {'k': 'Лови камень, федя!',
       'n': 'Ножнички, еба!',
       'b': 'Хоба, бумага, ёпта!'}

@bot.message_handler(content_types=["text"])
def any_msg(message):
    # Создаем клавиатуру и каждую из кнопок (по 2 в ряд)
    keyboard =telebot.types.InlineKeyboardMarkup(row_width=3)
    # url_button =telebot.types.InlineKeyboardButton(text="URL", url="https://ya.ru")
    # callback_button =telebot.types.InlineKeyboardButton(text="Callback", callback_data="test")
    # switch_button =telebot.types.InlineKeyboardButton(text="Switch", switch_inline_query="Telegram")
    stone = telebot.types.InlineKeyboardButton(text="Камень", callback_data="k")
    scissors = telebot.types.InlineKeyboardButton(text="Ножницы", callback_data="n")
    paper = telebot.types.InlineKeyboardButton(text="Бумага", callback_data="b")
    keyboard.add(stone, scissors, paper)
    bot.send_message(message.chat.id, "Жми, ёкарный бабай, жми!!!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        y = random.choice(['k','n','b'])
        bot.send_message(call.message.chat.id, DIC[y])
        x = call.data
        if x == y:
           result = 'Нихуя'
        elif (x == 'k' and y == 'n') or (x == 'n' and y == 'b') or (x == 'b' and y == 'k'):
           result = 'Заебал'
        else:
           result = 'Проебал'
        bot.send_message(call.message.chat.id, result)
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result)
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
        stone = telebot.types.InlineKeyboardButton(text="Камень", callback_data="k")
        scissors = telebot.types.InlineKeyboardButton(text="Ножницы", callback_data="n")
        paper = telebot.types.InlineKeyboardButton(text="Бумага", callback_data="b")
        keyboard.add(stone, scissors, paper)
        bot.send_message(call.message.chat.id, "Давай ещё жми!!!", reply_markup=keyboard)
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")


# Простейший инлайн-хэндлер для ненулевых запросов
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb =telebot.types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = []
    # Обратите внимание: вместо текста - объект input_message_content c текстом!
    single_msg =telebot.types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=10)