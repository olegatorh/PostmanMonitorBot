import sqlite3

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db', isolation_level=None, check_same_thread=False)
    cursor = sqlite_connection.cursor()

    print("База данных подключена к SQLite")
    sqlite_connection.commit()


except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        print("Соединение с SQLite закрыто")


def check_user(message):
    user_info = cursor.execute(
        "SELECT auto_sending, only_errors, full_info, server_update_info FROM users WHERE telegram_id = ?",
        (message["from"].id,)).fetchone()
    if user_info is None:
        cursor.execute(
            "INSERT OR IGNORE INTO users (name, joining_date, telegram_id) VALUES (?, ?, ?)",
            (message['from'].username,
             message.date.strftime('%Y-%m-%d'),
             message['from'].id,))
        user_info = cursor.execute("SELECT auto_sending, only_errors, full_info, server_update_info FROM users WHERE telegram_id = ?",
                                   message["from"].id, ).fetchone()
        return user_info
    else:
        return user_info


def change_user_settings(column, value, telegram_id):
    cursor.execute(f"UPDATE OR IGNORE users SET {column} = {value} WHERE telegram_id = {telegram_id}").fetchone()


def get_all_users():
    users = cursor.execute("SELECT * FROM users").fetchall()
    return users


def get_all_users_telegram_id():
    users = cursor.execute("SELECT telegram_id FROM users").fetchall()
    return users
