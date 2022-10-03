import telebot
from telebot import types
import config
import requests
import database
import sqlite3

connect = sqlite3.connect('C:/Users/lnlnl/Desktop/bot/db/dbForBot.db', check_same_thread=False)
cursor = connect.cursor()

bot = telebot.TeleBot(config.tken_bot)

apiKey = "9005b1597fff4141a27edf5fa19e3112"

news = []
country = "ru"
category = "technology"

def convert_list(new):
    str = ''
    for i in new:
        str += i + "\n"
    return str

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Добро пожаловать в MooreNews, " + message.from_user.first_name + "!")
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    exist_Us = database.exist_User(us_id);
    if (exist_Us == None):
        database.users_db(us_id, us_name)
    # BUTTON
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    show_news = types.KeyboardButton('Показать новости')
    subscription_management = types.KeyboardButton('Управление подписками')
    markup.add(show_news, subscription_management)
    bot.send_message(message.chat.id, "Доступные функции:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_news(message):
    if(message.text == "Показать новости"):
        a = requests.get(
            f'https://newsapi.org/v2/top-headlines/?apiKey={apiKey}&country={country}&category={category}&pageSize=2')
        for i in a.json()['articles']:
            news.append([i['title'], i['url']])
        answer = ""
        for line in news:
            answer += convert_list(line) + "\n"
        bot.send_message(message.chat.id, answer)
    elif (message.text == "Управление подписками"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        my_subscription = types.KeyboardButton('Мои подписки')
        subscribe = types.KeyboardButton('Подписаться')
        unsubscribe = types.KeyboardButton('Отписаться')
        back = types.KeyboardButton('Назад')
        markup.add(my_subscription, subscribe, unsubscribe, back)
        # btns=(my_subscription, subscribe, unsubscribe, back)
        # markup.add(btns)
        bot.send_message(message.chat.id, "Доступные функции:", reply_markup=markup)
    elif (message.text == "Подписаться"):
        cats = database.find_categories(cursor)
        print(cats)
        for item in cats:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(item[1])
            print(item[1])
            markup.add(btn)
        bot.send_message(message.chat.id, "Доступные категории:", reply_markup=markup)


bot.polling()
