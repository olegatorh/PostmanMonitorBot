import sqlite3
from datetime import datetime
from sqlite3 import IntegrityError

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db', isolation_level=None, check_same_thread=False)
    cursor = sqlite_connection.cursor()
    try:
        sqlite_create_table_query = '''CREATE TABLE api_list (
                                            id INTEGER PRIMARY KEY,
                                            api_name TEXT NOT NULL UNIQUE,
                                            api_url TEXT NOT NULL,
                                            notation TEXT(100),
                                            date datetime
                                            );'''
        cursor.execute(sqlite_create_table_query)

        sqlite_create_table_query = '''CREATE TABLE api_funcs (
                                                    id INTEGER PRIMARY KEY,
                                                    name TEXT NOT NULL,
                                                    type INTEGER NOT NULL,
                                                    headers TEXT,
                                                    date datetime,
                                                    params TEXT,
                                                    body TEXT,
                                                    notation TEXT(100),
                                                    api TEXT NOT NULL UNIQUE,
                                                    FOREIGN KEY(api) REFERENCES api_list(api_name)
                                                    );'''
        cursor.execute(sqlite_create_table_query)
    except Exception as e:
        print(e)

    print("База данных подключена к SQLite")
    sqlite_connection.commit()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        print("Соединение с SQLite закрыто")


def add_api_to_database(data):
    try:
        cursor.execute("insert into api_list(api_name, api_url, notation, date) VALUES (?,?,?,?)", (data["api_name"], data["api_url"], data["api_notation"], datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M')))
        response = cursor.execute(f"select * from api_list where api_name = ?", (data['api_name'],)).fetchone()
        return response
    except IntegrityError:
        print(f'error! (api name already used in database){IntegrityError}')
        return 'this name already used in database!'


def get_all_api():
    return cursor.execute("select * from api_list").fetchall()


def delete_api(api_name):
    print(api_name)
    cursor.execute(f"delete from api_list where api_name=?", (api_name, ))



def add_api_function_to_db(api, name):
    pass