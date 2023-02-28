from app import app
from flask import render_template, request, redirect, session
import users
from db import db
from users import register, login
from sqlalchemy.sql import text
from choose import showall, random, decide_self
import moods
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/new", methods =["GET","POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        nimi = request.form["nimi"]
        kategoria = request.form["kategoria"]
        hinta = request.form["kustannus"]
        free, lowcost, highcost = False
        if hinta == "Ilmainen":
            free = True
        if hinta == "Edullinen":
            lowcost = True
        if hinta == "Kallis":
            highcost = True

        sql = "INSERT INTO actions (name, category, free, lowcost, highcost) VALUES (:name, :category, :free, :lowcost, :highcost)"
        sql2 = text(sql)
        db.session.execute(sql2, {"name": name, "category": category, "free": free, "lowcost": lowcost, "highcost": highcost})
        db.session.commit()
        return render_template("acitivity_list.html")
        

@app.route("/create", methods=["GET","POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        nimi = request.form["nimi"]
        kategoria = request.form["kategoria"]
        kustannus = request.form["kustannus"]
        return render_template("/activity.html", nimi=nimi, kategoria=kategoria, kustannus=kustannus)

@app.route("/activity")
def activity(nimi, kategoria, kustannus):
    return render_template("activity.html", nimi = nimi, kategoria=kategoria, kustannus=kustannus)

@app.route("/logout")
def logout():
    del session["username"]
    
    return redirect("/")

@app.route("/decision", methods=["GET", "POST"])
def decision():
    if request.method == "GET":
        return render_template("decision.html")
    if request.method == "POST":
        return render_template("choose.html")

@app.route("/choose", methods=["GET", "POST"])
def choose():
    if request.method == "GET":
        return render_template("choose.html")
    if request.method == "POST":
        categories = request.form["kategoria"]
        prices = request.form["kustannus"]

        
        valinta = request.form["valinta"]
        if valinta == "showall":
            return render_template("showall.html")
        if valinta == "decide":
            free = False
            lowcost = False
            highcost = False
            for price in prices:
                if price == 1:
                    free = True
                if price == 2:
                    lowcost = True
                if price == 3:
                    highcost = True
            
            activities_list = decide_self(categories, free, lowcost, highcost)  
            return render_template("activity_list.html", activities_list = activities_list)
        if valinta =="random":
            free = False
            lowcost = False
            highcost = False
            for price in prices:
                if price == 1:
                    free = True
                if price == 2:
                    lowcost = True
                if price == 3:
                    highcost = True
            chosen = random(categories, free, lowcost, highcost)
            return render_template("activity.html")


@app.route("/review", methods=["GET"])
def review(name=None):

    activity_name = name
    review = request.form["effect"]
    if review == 1:
        effects.add_review(activity_name, True, False, False)
    elif review == 2:
        effects.add_review(activity_name, False, True, False)
    else:
        effects.add_review(activity_name, False, False, True)
    return render_template("effects.html")

@app.route("/moods", methods=["GET","POST"])
def mood():
    if request.method == "GET":
        return render_template("moods.html")
    if request.method == "POST":
        user_id = users.user_id()
        mood = request.form["mood"]
        intmood = int(mood)
        moods.add_mood(mood, user_id)
        return redirect("/")

@app.route("/showall")
def showall():
    sql = "SELECT * FROM actions"
    sql2 = "SELECT * FROM private_actions"
    return redirect("/")

@app.route("/activity_list")
def activity_list():
    return render_template("activity_list.html")
