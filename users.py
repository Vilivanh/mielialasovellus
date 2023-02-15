import os
from db import db
from flask import Flask
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv
 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///vanhav"
app.secret_key = getenv("SECRET_KEY")

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    sql2 = text(sql)
    result = db.session.execute(sql2, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = username
    session["csrf_token"] = os.urandom(16).hex()
    return True

def user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]
    del session["user_name"]

def register(name, password):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (name, password)
                 VALUES (:name, :password)"""
        sql2 = text(sql)
        db.session.execute(sql2, {"name":name, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(name, password)


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
