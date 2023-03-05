import os
from db import db
from flask import Flask
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv



def supervisor_login():
    username = request.form["username"]
    password = request.form["password"]
    session["csrf_token"] = secrets.token_hex(16)
    sql = "SELECT * FROM supervisors WHERE username = :username"
    sql2 = text(sql)
    user = db.session.execute(sql2, {"username": username}).fetchone()
    session["username"] = username
    sql = "SELECT id FROM supervisors WHERE username = :username"
    sql2 = text(sql)
    user_id = db.session.execute(sql2, {"username": username}).fetchone()[0]
    session["user_id"] = user_id
       



def supervisor_registration():
    username = request.form["username"]
    if len(username) < 2 or len(username) > 20:
        return render_template("error.html", message = "Tunnuksessa tulee olla 2-20 merkkiä")
    pass1 = request.form["password1"]
    pass2 = request.form["password2"]
    validate = request.form["validation"]
    print(validate)
    if validate != "IsoPahaPunainenKissa":
        return render_template("error.html", message = "et ole oikeutettu ryhtymään ylläpitäjäksi")
    if pass1 != pass2:
         return render_template("error.html", message = "salasanat eivät vastaa toisiaan")
    if pass1 == "":
        return render_template("error.html", message = "salasana ei voi olla tyhjä")
    #if not users.register(username, pass1):
        #return render_template("error.html", message = "rekisteröinti epäonnistui"
    hash_value = generate_password_hash(pass1)
    sql = "INSERT INTO supervisors (username, password) VALUES (:username, :password)"
    sql2 = text(sql)
    result = db.session.execute(sql2, {"username": username, "password": hash_value})
    db.session.commit()
    session["username"] = username
    sql3 = "SELECT id FROM supervisors WHERE username = :username"
    sql4 = text(sql3)
    user_id = db.session.execute(sql4, {"username": username}).fetchone()
    session["user_id"] = int(user_id[0])
      



def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        name = request.form["name"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if len(name) > 80:
            return render_template("error.html", message = "aktiviteetin nimi on liian pitkä")
        category = request.form["category"]
        price = request.form["price"]
        free, lowcost, highcost = False
        if price == "Ilmainen":
            free = True
        if price == "Edullinen":
            lowcost = True
        if price == "Kallis":
            highcost = True
        sql = "INSERT INTO actions (name, category, free, lowcost, highcost) VALUES (:name, :category, :free, :lowcost, :highcost)"
        sql2 = text(sql)
        db.session.execute(sql2, {"name": name, "category": category, "free": free, "lowcost": lowcost, "highcost": highcost})
        db.session.commit()
        return render_template("activity.html", name=name, category=category, price=price)
