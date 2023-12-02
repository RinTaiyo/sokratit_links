import random
import hashlib
import sqlite3
import flask
from flask import Flask, render_template, request, session, redirect, jsonify
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
import database as db

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
db.create()


@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    s = "www"
    short_url = s

    return jsonify({'short_url': short_url}), 200


@app.route('/reg', methods=['POST', 'GET'])
def register():
    print('123')
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    print(login, password)

    result = db.selectUser(login)

    if result:
        return "Пользователь уже зарегистрирован"
    else:
        password_hash = generate_password_hash(password)
        db.register(login,password_hash)
        return "success"




@app.route('/aut', methods=['GET', 'POST'])
def aut():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    result = db.selectUser(login)
    if result and check_password_hash(result[2], password):
        token=create_access_token(identity=login)
        return f"Вы авторизованы\n{token}"
    else:
        return "Неправильный логин или пароль"




@app.route('/lk', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
def lk():
    user = get_jwt_identity()
    result = db.selectUser(user)
    user_id = result[0]
    print(user, user_id)
    if request.method == 'POST':
        long_url = request.json.get("long", None)
        access_url=request.json.get("access", None)
        short_link=request.json.get("short", None)
        print(long_url, access_url)
        if short_link=="":
            short_url=hashlib.md5(long_url.encode()).hexdigest()[:random.randint(8,12)]
        else:

            short_url=short_link
        print(short_url, user_id)
        if db.checkShort(short_url)==True:
        # db.addLongLinkAndShort(long_url, short_url,access_url,user_id)
            db.addLongLinkAndShort(long_url, short_url, access_url, user_id)
            return 'success'
        else:
            return 'not unique'


       # db.sokrat()
    elif request.method == 'DELETE':
        short_link=request.json.get("short", None)
        if db.findLinkShort(short_link, user_id):
            db.delete_long_url(short_link)
            return 'Ссылка удалена'
        else:
            return 'не найдено'
    elif request.method == 'GET':
        user = get_jwt_identity()
        myLinks = db.watchLk(user_id)
        print('123\n',myLinks)

        if myLinks:
            myLinksBeaty = []

            for row in myLinks:
                link = {}
                link["Long URL"] = row[1]
                link["Short URL"] = row[2]
                link["Access level"] = row[7]
                link["Count"] = row[4]
                link["User id"] = row[5] # ??? не факт что 5

                myLinksBeaty.append(link)

#
          #  for link in myLinksBeaty:
              #  print(link)
             #   authorized_links = []
             #   for link in myLinksBeaty:
                  #  if link["Access level"] == 1 or (link["Access level"] == 2 and user_id == link["user_id"]) or (
                  #  link["Access level"] == 3):
                      #  authorized_links.append(link)

          #  return authorized_links
            return myLinksBeaty
        else:
            return 'У вас похоже нет пока ссылок'

    elif request.method == 'PUT':
            short_link = request.json.get("short link", None)
            short_link_new = request.json.get("short link new", None)
            access = request.json.get("access", None)
            id_link =db.findLinkShort(short_link, user_id)
            if id_link:

                if short_link == "":
                    return "Поле короткая ссылка не может быть пустым"
                elif short_link_new=="" and access =="":
                    return "Одно из полей обязательно должно быть заполнено"
                else:
                    if not (access == ""):
                        db.updateLinkAccess(id_link, access) # обновляем
                    if not (short_link_new == "") :
                        db.updateLinkShort(id_link, short_link_new)  # обновляем
                    return 'success'
            else:
                return 'ссылка не найдена'






# @app.route('/lvl', methods=['GET', 'PUT'])
# @jwt_required(optional=True)
# def lvl():
#     user = get_jwt_identity()
#     if user:
#         db.watchLink2()"


@app.route('/delUser', methods=['GET', 'POST'])
def delUser():
    db.delete_user()

#@app.route('/delLn', methods=[ 'DELETE'])
#def dellinks():
    #db.delete_long_url()
   # return 'Ссылка удалена'


@app.route('/<short_link>', methods=['GET'])
@jwt_required(optional=True)
def red(short_link):
    # print('!!!')
    LinksList = db.vstavkaLink(short_link)


    user=get_jwt_identity()
    # print('!!!',user)
    # prov2=db.watchLk(user_id)
    # print(prov2)
    # print(LinksList)

    if LinksList["access_id"]==1:
        return redirect(LinksList["long"])


    elif LinksList["access_id"]==3:
        if user == None:
            return 'Авторизуйтесь'
        else:
            return redirect(LinksList["long"])


    elif LinksList["access_id"]==2:
        if user is not None and LinksList["user_id"]==db.selectUser(user)[0]:
            return redirect(LinksList["long"])
        elif user is not None and not (LinksList["user_id"]==db.selectUser(user)[0]):
           return "Вы не владелец данной ссылки"
        else:
            return "Авторизуйтесь"




    # if link == "gg":
    #     end = "https://www.google.com/"
    #     return redirect(end)
    # else:
    #     return "not found"


if __name__ == '__main__':
    app.run(debug=True)
