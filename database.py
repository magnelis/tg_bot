import sqlite3

connect = sqlite3.connect('C:/Users/lnlnl/Desktop/bot/db/dbForBot.db', check_same_thread=False)
cursor = connect.cursor()


# ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ В БД
def add_users_in_db(user_id, name_user):
    cursor.execute('INSERT INTO users (user_id, name_user) VALUES (?, ?)', (user_id, name_user))
    connect.commit()


# ПОИСК ПОЛЬЗОВАТЕЛЯ В БД
def exist_user(user_id):
    sql = "SELECT users.user_id FROM users WHERE user_id=:user_id"
    result = cursor.execute(sql, {'user_id': user_id}).fetchone()
    connect.commit()
    return result


# ВЫВОД ВСЕХ КАТЕГОРИЙ
def find_categories():
    result = cursor.execute("SELECT categories.* FROM categories").fetchall()
    connect.commit()
    return result


# ПОДПИСКА ПОЛЬЗОВАТЕЛЯ НА КАТЕГОРИЮ
def add_subscr(user_id, category_name):
    sql = "INSERT INTO subscriptions (user_id, category_name) VALUES (:user_id, :category_name)";
    cursor.execute(sql, {'user_id': user_id, 'category_name': category_name})
    connect.commit()


# ПОИСК КАТЕГОРИИ ПО ПОЛЬЗОВАТЕЛЮ
def find_subscr(user_id):
    sql = "SELECT subscriptions.category_name FROM subscriptions WHERE user_id = :user_id"
    result = cursor.execute(sql, {'user_id': user_id}).fetchall()
    connect.commit()
    return result


# ПОИСК КАТЕГОРИИ
def find_id_cat(user_id, category_name):
    sql = "SELECT subscriptions.category_name FROM subscriptions WHERE user_id = :user_id AND category_name =:category_name"
    result = cursor.execute(sql, {'user_id': user_id, 'category_name': category_name}).fetchone();
    connect.commit();
    return result;


def unsub_cat(user_id, category_name):
    sql = "DELETE FROM subscriptions WHERE user_id=:user_id and category_name =:category_name";
    cursor.execute(sql, {'user_id': user_id, 'category_name': category_name});
    connect.commit();
