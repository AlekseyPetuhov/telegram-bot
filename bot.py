# _*_ coding : utf-8 _*_


import telebot
from telebot import types
import config
import xml.etree.ElementTree as ET
from urllib.request import urlopen

bot = telebot.TeleBot(config.token)
i = 0


def get_valutes():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    with urlopen(url, timeout=10) as usd:
        current_value_usd = ET.parse(usd).findtext('.//Valute[@ID="R01235"]/Value')
        str_usd = 'USD: ' + current_value_usd
        print(str_usd)

    with urlopen(url, timeout=10) as eur:
        current_value_eur = ET.parse(eur).findtext('.//Valute[@ID="R01239"]/Value')
        str_eur = 'EUR: ' + current_value_eur
        print(str_eur)

    return str_usd + "\n" + str_eur


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/help', '/hide')
    bot.send_message(message.chat.id, 'Добро пожаловать!'
                                      '\nЯ умею показывать текущие курсы валют, а чуть позже научусь сохранять заметки и '
                                      'создавать напоминания.'
                                      '\nДля получения справки введите /help', reply_markup=user_markup)
    print(message.chat.id)


@bot.message_handler(commands=['help'])
def handle_text(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Текстовые команды')
    user_markup.row('Команды')
    bot.send_message(message.chat.id, """Все взаимодействие происходит с помощью команд. Я понимаю текстовые команды, и команды из меню.
Для просмотра списка текстовых команд нажмите на кнопку \"Текстовые команды\". Для перехода к меню, нажмите на кнопку 
\"Команды\".""", reply_markup=user_markup)


@bot.message_handler(commands=['hide'])
def handle_hide(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Клавиатура убрана', reply_markup=hide_markup)


@bot.message_handler(commands=['valutes'])
def handle_text(message):
    bot.send_message(message.chat.id, get_valutes())


@bot.message_handler(content_types=['text'])
def handle_text(message):
    name_note = message.text
    if message.text == "Курс валют":
        bot.send_message(message.chat.id, get_valutes())
    if message.text == "Текстовые команды":
        bot.send_message(message.chat.id, 'На данный момент, доступны следующие текстовые комманды:'
                                          '\n/help - Получение справки'
                                          '\nКурс валют - Получение текущего курса валют'
                                          '\nКоманды - вызов меню')
    if message.text == "Команды":
        kb = telebot.types.InlineKeyboardMarkup()
        valute_button = types.InlineKeyboardButton(text="Курс валют", callback_data="val")
        kb.add(valute_button)
        bot.send_message(message.chat.id, "Список команд", reply_markup=kb)
    # if message.text == "Команды":
    #     kb = telebot.types.ReplyKeyboardMarkup(True, False)
    #     kb.row("Курс валют")
    #     bot.send_message(message.chat.id, "Список команд", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "val":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=get_valutes())

    elif call.inline_message_id:
        if call.data == "val":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text=get_valutes())


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
