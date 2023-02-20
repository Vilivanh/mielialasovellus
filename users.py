import os
from db import db
from flask import Flask
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv
 

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")

def login(username, password):
    sql = "SELECT password, id FROM users WERE username=:username"
    sql2 = text(sql)
    print(sql)
    print(sql2)
    result = db.session.execute(sql2, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user[0], password):
        session["userid"] = user[1]
        session["username"] = username
        session["csrf_token"] = os.urandom(16).hex()
        return True
    else:
        return False

def user_id():
    return session.get("userid", 0)

def logout():
    del session["userid"]
    del session["username"]

def register(username, password):
    hash_value = generate_password_hash(password)

    try:
        sql = """INSERT INTO users (username, password)
                 VALUES (:username, :password)"""
        sql2 = text(sql)
        db.session.execute(sql2, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
