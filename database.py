import sqlite3
path='database.db'
accesses={
    1:"публичный доступ",
    2:"приватный доступ",
    3:"общедоступный доступ"
}

def get_key(slovar, znachenie):
    for key, value in slovar.items():
        if value==znachenie:
            return key

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

    cursor.execute('''SELECT COUNT(*) FROM access''')
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute('insert into access (name) values ("публичный доступ")')
        cursor.execute('insert into access (name) values ("приватный доступ")')
        cursor.execute('insert into access (name) values ("общедоступный доступ")')
        connect.commit()


    connect.close()


def register(log, passw):
    connect = sqlite3.connect(path)
    cursor = connect.cursor()
    cursor.execute('''
    insert into users (login, password) values (?,?)
    ''', (log, passw))
    connect.commit()
    connect.close()


def delete_user(login, password):
    connect = sqlite3.connect(path)
    cursor = connect.cursor()
    cursor.execute('''DELETE FROM users WHERE login=? AND password=?;''', (login, password))
    connect.close()


def selectUser(login):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE login = ? "
    cursor.execute(query, (login,))
    result = cursor.fetchone()
    return result
def deleteLk():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    query = "DELETE FROM link WHERE id = ?"
    cursor.execute(query, (id,))
    conn.commit()
    conn.close()
def watchLk(id):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    query = "SELECT * FROM links JOIN access ON links.access_id = access.id WHERE links.user_id=?"
    answer = cursor.execute(query, (id,)).fetchall()
    conn.close()
    return answer


#объединяем таблицы links и access по полю access_id, чтобы получить уровень доступа к каждой ссылке.
def watchLinks():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    query = ("SELECT links.long, links.short, access.name, "
             "links.count FROM links JOIN access ON links.access_id = access.id WHERE links.user_id = <id=1>")

def watchLink2():
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    query = ("SELECT long, short FROM links INNER JOIN access ON links.access_id = access.id WHERE access.name = 'публичный' ")

def addLongLinkAndShort(long_url, short_url, access_url, user_id):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    access_id=get_key(accesses, access_url)
    cursor.execute("INSERT INTO links (long, short, access_id, count, user_id) VALUES (?,?,?,0,?)", (long_url,short_url, access_id, user_id) )

    conn.commit()

def checkShort(short):
    short=(short,)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    checkResult=cursor.execute("""
    SELECT short from links""").fetchall()
    conn.commit()
    if short in checkResult:
        return False
    else:
        return True



def delete_long_url(short_url):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # запрос на удаление данных из таблицы
    cursor.execute("DELETE FROM links WHERE short=?", (short_url,))
    conn.commit()
    conn.close()

def findLinkShort(short_link, user_id):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    result = cursor.execute("SELECT links.id FROM links where short=? and user_id=?",
                   (short_link,user_id)).fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return False
def updateLinkAccess(id_link, access):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    access_id = get_key(accesses, access)
    cursor.execute("UPDATE links SET access_id= ? WHERE id = ?", (access_id,id_link ))

    conn.commit()
    conn.close()
def addLongLinkAndLvl(long_url, access_lvl):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (long, access_id) VALUES (?, ?)", (long_url, access_lvl))
    conn.commit()

def addShortLink(short_url, last_id):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("UPDATE links SET short = ? WHERE id = ?", (short_url, last_id))
    conn.commit()
def updateLinkShort(id_link, short_link_new):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("UPDATE links SET short = ? WHERE id = ?", (short_link_new,id_link))
    conn.commit()
    conn.close()
def vstavkaLink(short_link):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    result = cursor.execute("SELECT short, long, user_id, access_id FROM links INNER JOIN access ON"
                            " links.access_id = access.id WHERE short=?",

                            (short_link, )).fetchone()


    conn.close()
    if result is not None:
        return {
            "short":result[0],
            "long":result[1],
            "user_id":result[2],
            "access_id":result[3],
        }
    else:
        return False
