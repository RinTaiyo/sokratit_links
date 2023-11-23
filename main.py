import random
import hashlib
import sqlite3
import flask
from flask import Flask, render_template, request, session, redirect, jsonify
from flask_jwt_extended import create_access_token, JWTManager, get_jwt_identity, jwt_required
import database as db

app = Flask(__name__)
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

    result=db.selectUser(login,password)

    if result:
        print("Пользователь уже зарегистрирован")
    else:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        db.register(login,password)
        return "success"




@app.route('/aut', methods=['GET'])
def aut():
    conn= sqlite3.connect('database.py')



    cursor = conn.cursor()

    login = input("Введите логин: ")
    password = input("Введите пароль: ")

    query = "SELECT * FROM users WHERE login = ? AND password = ?"
    cursor.execute(query, (login, password))
    result = cursor.fetchone()

    if result:
        print("Вы авторизованы")
    else:
        print("Неправильный логин или пароль")

    conn.close()


@app.route('/lk', methods=['POST', 'GET', 'PUT', 'DELETE'])
def lk():
    if request.method=='POST':
        pass
    elif request.method=='DELETE':
        db.deleteLk()
    elif request.method=='GET':
        db.watchLk()
    elif request.method=='PUT':
       pass

@app.route('/<link>', methods=['GET'])
def red(link):
    if link == "gg":
        end = "https://www.google.com/"
        return redirect(end)
    else:
        return "not found"


if __name__ == '__main__':
    app.run(debug=True)