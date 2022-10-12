import telebot
import config
import requests
import database
from telebot import types

bot = telebot.TeleBot(config.tken_bot)

apiKey = "Вставьте свой api"

country = "ru"
category = "technology"


# ФУНКЦИИ
def convert_list(new):
    str = ''
    for i in new:
        str += i + "\n"
    return str


def sub(user_id, category, call):
    if (database.find_id_cat(user_id, category) == None):
        database.add_subscr(call.from_user.id, category)
        bot.answer_callback_query(call.id, text="Вы успешно подписались!")
    else:
        bot.answer_callback_query(call.id, show_alert=True, text="Вы уже подписаны на эту категорию.")


def get_news(category):
    a = requests.get(
        f'https://newsapi.org/v2/top-headlines/?apiKey={apiKey}&country={country}&category={category}&pageSize=2')
    news = []
    for i in a.json()['articles']:
        news.append([i['title'], i['url']])
    answer = ""
    for line in news:
        answer += convert_list(line) + "\n"
    return answer


def btn_redraw(call, user_id):
    bot.answer_callback_query(call.id, text="Вы успешно отписались!")
    bot.delete_message(call.message.chat.id, call.message.message_id)
    cats = database.find_subscr(user_id)
    markup = types.InlineKeyboardMarkup()
    for item in cats:
        markup.add(types.InlineKeyboardButton(item[0], callback_data=f'unsub-{item[0]}'))
    bot.send_message(call.message.chat.id, "Категории, на которые вы подписаны:", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Добро пожаловать в MooreNews, " + message.from_user.first_name + "!")
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    exist_us = database.exist_user(user_id);
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
    category = database.find_subscr(user_id)

    # ПОКАЗАТЬ НОВОСТИ
    if (message.text == "Показать новости"):
        cats = database.find_subscr(user_id)
        markup = types.InlineKeyboardMarkup()
        for item in cats:
            markup.add(types.InlineKeyboardButton(item[0], callback_data=f'news-{item[0]}'))
        bot.send_message(message.chat.id, "Доступные категории:", reply_markup=markup)

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
            markup.add(types.InlineKeyboardButton(item[1], callback_data=f'sub-{item[1]}'))
        bot.send_message(message.chat.id, "Доступные категории:", reply_markup=markup)
    # ОТПИСАТЬСЯ
    elif (message.text == "Отписаться"):
        cats = database.find_subscr(user_id)
        markup = types.InlineKeyboardMarkup()
        for item in cats:
            markup.add(types.InlineKeyboardButton(item[0], callback_data=f'unsub-{item[0]}'))
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
    command = call.data.split('-')[0]
    data = call.data.split('-')[1]
    user_id = call.from_user.id

    if (command == 'sub'):
        if data == 'science':
            sub(user_id, data, call)
        elif data == 'business':
            sub(user_id, data, call)
        elif data == 'health':
            sub(user_id, data, call)
        elif data == 'general':
            sub(user_id, data, call)
        elif data == 'technology':
            sub(user_id, data, call)
        elif data == 'sports':
            sub(user_id, data, call)

    elif (command == 'unsub'):
        if data == 'science':
            database.unsub_cat(user_id, data)
            btn_redraw(call, user_id)
        elif data == 'business':
            database.unsub_cat(user_id, data)
            btn_redraw(call, user_id)
        elif data == 'health':
            database.unsub_cat(user_id, data)
            btn_redraw(call, user_id)
        elif data == 'general':
            database.unsub_cat(user_id, data)
            btn_redraw(call, user_id)
        elif data == 'technology':
            database.unsub_cat(user_id, data)
            btn_redraw(call, user_id)
        elif data == 'sports':
            database.unsub_cat(user_id, data)
            btn_redraw(call, user_id)

    elif (command == 'news'):
        if data == 'science':
            bot.send_message(call.message.chat.id, get_news(data))
        elif data == 'business':
            bot.send_message(call.message.chat.id, get_news(data))
        elif data == 'health':
            bot.send_message(call.message.chat.id, get_news(data))
        elif data == 'general':
            bot.send_message(call.message.chat.id, get_news(data))
        elif data == 'technology':
            bot.send_message(call.message.chat.id, get_news(data))
        elif data == 'sports':
            bot.send_message(call.message.chat.id, get_news(data))


bot.polling()
