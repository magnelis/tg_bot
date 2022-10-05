import telebot
import config
import requests
import database
from telebot import types

bot = telebot.TeleBot(config.tken_bot)

apiKey = "9005b1597fff4141a27edf5fa19e3112"

news = []
country = "ru"
category = "technology"

# ФУНКЦИИ
def convert_list(new):
    str = ''
    for i in new:
        str += i + "\n"
    return str

def sub(user_id, category):
    if (database.findIdCat(user_id, category.data) == None):
        database.add_subscr(category.from_user.id, category.data)
        bot.answer_callback_query(category.id, text="Вы успешно подписались!")
    else:
        bot.answer_callback_query(category.id, show_alert=True, text="Вы уже подписаны на эту категорию.")

@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Добро пожаловать в MooreNews, " + message.from_user.first_name + "!")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    exist_us = database.exist_User(user_id);
    if (exist_us == None):
        database.add_users_in_db(user_id, user_name)
    # КНОПКИ
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if (database.find_subscr(user_id) != None):
        show_news = types.KeyboardButton('Показать новости')
        subscription_management = types.KeyboardButton('Управление подписками')
        markup.add(show_news, subscription_management)
        bot.send_message(message.chat.id, "Доступные функции:", reply_markup=markup)
    else:
        subscription_management = types.KeyboardButton('Управление подписками')
        markup.add(subscription_management)
        bot.send_message(message.chat.id, "Доступные функции:", reply_markup=markup)

# РАБОТА С КНОПКАМИ
@bot.message_handler(content_types=['text'])
def send_news(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # ПОКАЗАТЬ НОВОСТИ
    if(message.text == "Показать новости"):
        a = requests.get(f'https://newsapi.org/v2/top-headlines/?apiKey={apiKey}&country={country}&category={category}&pageSize=2')
        for i in a.json()['articles']:
            news.append([i['title'], i['url']])
        answer = ""
        for line in news:
            answer += convert_list(line) + "\n"
        bot.send_message(message.chat.id, answer)
    # УПРАВЛЕНИЕ ПОДПИСКАМИ
    elif (message.text == "Управление подписками"):
        my_subscription = types.KeyboardButton('Мои подписки')
        subscribe = types.KeyboardButton('Подписаться')
        unsubscribe = types.KeyboardButton('Отписаться')
        back = types.KeyboardButton('Назад')
        markup.add(my_subscription, subscribe, unsubscribe, back)
        bot.send_message(message.chat.id, "Доступные функции:", reply_markup=markup)
    # МОИ ПОДПИСКИ
    elif (message.text == "Мои подписки"):
        user_subscriptions = database.find_subscr(user_id)
        if (user_subscriptions == None):
            bot.send_message(message.chat.id, "Вы не подписаны ни на одну категорию.")
        else:
            answer = ""
            for line in user_subscriptions:
                answer += convert_list(line)
            bot.send_message(message.chat.id, answer)
    # ПОДПИСАТЬСЯ
    elif (message.text == "Подписаться"):
        cats = database.find_categories()
        markup = types.InlineKeyboardMarkup()
        for item in cats:
            btn = item[1]
            markup.add(types.InlineKeyboardButton(btn, callback_data=btn))
        bot.send_message(message.chat.id, "Доступные категории:", reply_markup=markup)
    # ОТПИСАТЬСЯ
    elif (message.text == "Отписаться"):
        cats = database.find_subscr(user_id)
        markup = types.InlineKeyboardMarkup()
        for item in cats:
            btn2 = item[0]
            markup.add(types.InlineKeyboardButton(btn2, callback_data=btn2))
            print(btn2)
        bot.send_message(message.chat.id, "Категории, на которые вы подписаны:", reply_markup=markup)
    # НАЗАД
    elif (message.text == "Назад"):
        show_news = types.KeyboardButton('Показать новости')
        subscription_management = types.KeyboardButton('Управление подписками')
        markup.add(show_news, subscription_management)
        bot.send_message(message.chat.id, "Доступные функции:", reply_markup=markup)

# КНОПКИ С ПОДПИСКАМИ
@bot.callback_query_handler(func=lambda call: True)
def send_text(call):
    user_id = call.from_user.id
    if call.data == 'science':
        sub(user_id, call)
    elif call.data == 'business':
        sub(user_id, call)
    elif call.data == 'health':
        sub(user_id, call)
    elif call.data == 'general':
        sub(user_id, call)
    elif call.data == 'technology':
        sub(user_id, call)
    elif call.data == 'sports':
        sub(user_id, call)





bot.polling()
