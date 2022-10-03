import sqlite3

connect = sqlite3.connect('C:/Users/lnlnl/Desktop/bot/db/dbForBot.db', check_same_thread=False)
cursor = connect.cursor()

def users_db(user_id, name_user):
    cursor.execute('INSERT INTO users (user_id, name_user) VALUES (?, ?)', (user_id, name_user))
    connect.commit()

def exist_User(user_id):
    sql = "SELECT users.user_id FROM users WHERE user_id=:user_id"
    result = cursor.execute(sql, {'user_id':user_id}).fetchone()
    connect.commit()
    return result

def find_categories(cursor):
    result = cursor.execute("SELECT categories.* FROM categories").fetchall()
    connect.commit()
    return result
