from app import app
from flask import render_template, request, redirect, session
import users
from db import db
from users import register, login
from sqlalchemy.sql import text
from choose import showall, random, decide_self
import moods
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        if request.method == "POST":
                                username = request.form["username"]
                                        password = request.form["password"]
                                                sql = "SELECT * FROM users WHERE username = :username"
                                                        sql2 = text(sql)
                                                                user = db.session.execute(sql2, {"username": username}).fetchone()
                                                                        if user:
                                                                                        pw = user["password"]
                                                                                                #if not user:
                                                                                                            #return render_template("error.html", message="virheellinen kirjautumisyritys")
                                                                                                                    session["username"] = username
                                                                                                                            sql = "SELECT id FROM users WHERE username = :username"
                                                                                                                                    sql2 = text(sql)
                                                                                                                                            user_id = db.session.execute(sql2, {"username": username}).fetchone()
                                                                                                                                                    session["user_id"] = user_id
                                                                                                                                                            return redirect("/")


                                                                                                                                                        @app.route("/register", methods=["GET", "POST"])
                                                                                                                                                        def register():
                                                                                                                                                                if request.method == "GET":
                                                                                                                                                                            return render_template("register.html")
                                                                                                                                                                            if request.method == "POST":
                                                                                                                                                                                        username = request.form["username"]
                                                                                                                                                                                                if len(username) < 2 or len(username) > 20:
                                                                                                                                                                                                                return render_template("error.html", message = "Tunnuksessa tulee olla 2-20 merkkiä")
                                                                                                                                                                                                                    pass1 = request.form["password1"]
                                                                                                                                                                                                                            pass2 = request.form["password2"]
                                                                                                                                                                                                                                    if pass1 != pass2:
                                                                                                                                                                                                                                                    return render_template("error.html", message = "salasanat eivät vastaa toisiaan")
                                                                                                                                                                                                                                                        if pass1 == "":
                                                                                                                                                                                                                                                                        return render_template("error.html", message = "salasana ei voi olla tyhjä")
                                                                                                                                                                                                                                                                            #if not users.register(username, pass1):
                                                                                                                                                                                                                                                                                       # return render_template("error.html", message = "rekisteröinti epäonnistu")
                                                                                                                                                                                                                                                                                               hash_value = generate_password_hash(pass1)
                                                                                                                                                                                                                                                                                                       sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
                                                                                                                                                                                                                                                                                                               sql2 = text(sql)
                                                                                                                                                                                                                                                                                                                       result = db.session.execute(sql2, {"username": username, "password": hash_value})
                                                                                                                                                                                                                                                                                                                               db.session.commit()
                                                                                                                                                                                                                                                                                                                                       session["username"] = username
                                                                                                                                                                                                                                                                                                                                               sql3 = "SELECT id FROM users WHERE username = :username"
                                                                                                                                                                                                                                                                                                                                                       sql4 = text(sql3)
                                                                                                                                                                                                                                                                                                                                                               user_id = db.session.execute(sql4, {"username": username}).fetchone()
                                                                                                                                                                                                                                                                                                                                                                       session["user_id"] = int(user_id[0])
                                                                                                                                                                                                                                                                                                                                                                               return redirect("/")
