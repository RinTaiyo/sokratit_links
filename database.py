import sqlite3
path='database.db'
def create():
    connect = sqlite3.connect(path)
    cursor = connect.cursor()
    cursor.execute('''
    create table if not exists "users" (
    "id" integer not null,
    "login" text not null,
    "password" text not null,
    primary key ("id" autoincrement)
    );
    ''')
    connect.commit()


    cursor.execute('''
 create table if not exists "access" (
    "id" integer not null,
    "name" text not null,
    primary key ("id" autoincrement)
    );
    ''')
    connect.commit()


    cursor.execute('''
     create table if not exists "links" (
    "id" integer not null,
    "long" text not null,
    "short" text not null,

    "access_id" integer not null,
    "count" integer not null,
    "user_id" integer not null,
    primary key ("id" autoincrement)
    );
    ''')
    connect.commit()

    #заполнить таблицу access

    connect.close()

def register(log, passw):
    connect = sqlite3.connect(path)
    cursor = connect.cursor()
    cursor.execute('''
    insert into users (login, password) values (?,?)
    ''', (log, passw))
    connect.commit()
    connect.close()

def selectUser(login):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE login = ? "
    cursor.execute(query, (login,))
    result = cursor.fetchone()
    return result
def deleteLk():
    conn = sqlite3.connect('database.py')
    cursor = conn.cursor()
    query = "DELETE FROM link WHERE id = ?"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
def watchLk():
    conn = sqlite3.connect('database.py')
    cursor = conn.cursor()
    query = "SELECT * FROM link JOIN access ON link.id = access.link_id WHERE access.user_id=?"
    cursor.execute(query, (id,))
