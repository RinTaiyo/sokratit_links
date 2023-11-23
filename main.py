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
    print(result)
    if result and check_password_hash(result[2], password):
        token=create_access_token(identity=login)
        return f"Вы авторизованы\n{token}"
    else:
        return "Неправильный логин или пароль"




@app.route('/lk', methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
def lk():
    if request.method == 'POST':
        db.sokrat()
    elif request.method == 'DELETE':
        db.deleteLk()
    elif request.method == 'GET':
        user=get_jwt_identity()
        print(user)
        db.watchLk()
    elif request.method == 'PUT':
        db.putLk()

@app.route('/<link>', methods=['GET'])
def red(link):
    if link == "gg":
        end = "https://www.google.com/"
        return redirect(end)
    else:
        return "not found"

if __name__ == '__main__':
    app.run(debug=True)
