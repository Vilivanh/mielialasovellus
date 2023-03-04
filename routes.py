from app import app
from flask import render_template, request, redirect, session
import users
from db import db
from users import register, login
from effects import show_reviews, filter_reviews
from sqlalchemy.sql import text
from choose import showall, random_action, decide_self
from moods import add_mood, show_moods
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
from datetime import datetime
import secrets  

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
        session["csrf_token"] = secrets.token_hex(16)
        sql = "SELECT * FROM users WHERE username = :username"
        sql2 = text(sql)
        user = db.session.execute(sql2, {"username": username}).fetchone()
        #if user:
            #pw = user[2]
        #if not user:
            #return render_template("error.html", message="virheellinen kirjautumisyritys")
        session["username"] = username
        sql = "SELECT id FROM users WHERE username = :username"
        sql2 = text(sql)
        user_id = db.session.execute(sql2, {"username": username}).fetchone()[0]
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
        name = request.form["name"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        category = request.form["category"]
        price = request.form["price"]
        free, lowcost, highcost = False
        if price == "Ilmainen":
            free = True
        if price == "Edullinen":
            lowcost = True
        if price == "Kallis":
            highcost = True

        sql = "INSERT INTO private_actions (name, category, free, lowcost, highcost) VALUES (:name, :category, :free, :lowcost, :highcost)"
        sql2 = text(sql)
        db.session.execute(sql2, {"name": name, "category": category, "free": free, "lowcost": lowcost, "highcost": highcost})
        db.session.commit()
        return render_template("activity.html", name=name, category=category, price=price)
        

@app.route("/create", methods=["GET","POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        nimi = request.form["nimi"]
        kategoria = request.form["kategoria"]
        kustannus = request.form["kustannus"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        return render_template("/activity.html", nimi=nimi, kategoria=kategoria, kustannus=kustannus)

@app.route("/activity", methods=["GET","POST"])
def activity():
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("activity.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        name = request.form["name"]
        category=request.form["category"]
        price=request.form["price"]
        free = False
        lowcost = False
        highcost = False
        if price == "Ilmainen":
            free = True
        if price == "Edullinen":
            lowcost = True
        if price == "Kallis":
            highcost = True
        sql = "INSERT INTO private_actions (creator_id, name, category, free, lowcost, highcost) VALUES (:creator_id, :name, :category, :free, :lowcost, :highcost)"
        sql2 = text(sql)
        db.session.execute(sql2, {"creator_id": user_id, "name": name, "category": category, "free": free, "lowcost": lowcost, "highcost": highcost})
        db.session.commit()
        return render_template("activity.html", name = name, category = category, price=price)

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/decision", methods=["GET", "POST"])
def decision():
    if request.method == "GET":
        return render_template("decision.html")
    if request.method == "POST":
        return render_template("choose.html")

@app.route("/choose", methods=["GET", "POST"])
def choose():
    user_id = session["user_id"]
    if request.method == "GET":
        return render_template("choose.html")
    if request.method == "POST":        
        valinta = request.form["valinta"]
        if valinta == "showall":
            sql = "SELECT name, category, FROM actions UNION SELECT name, category FROM private_actions WHERE creator_id=user_id"
            sql2 = text(sql)
            results = db.session.execute(sql2, {"user_id": user_id}).fetchall()
            return render_template("showall.html", results=results)
        if valinta == "decide":
            prices = request.form.getlist("price")
            categories = request.form.getlist("categories")
            newlist = []
            if "Ilmainen" in prices:
                
                for category in categories:
                    sql = "SELECT name, category FROM actions WHERE category=:category AND free=TRUE UNION SELECT name, category FROM private_actions WHERE category=:category AND free=TRUE and creator_id=:user_id"
                    sql2 = text(sql)
                    results = db.session.execute(sql2, {"category": category, "user_id": user_id})
                    for result in results:
                        newlist.append(result[0], result[1], "Ilmainen")
            if "Edullinen" in prices:
                for category in categories:
                    sql = "SELECT name, category FROM actions WHERE category=:category AND lowcost=TRUE UNION SELECT name, category FROM private_actions WHERE category=:category AND lowcost=TRUE and creator_id=:user_id"
                    sql2 = text(sql)
                    results = db.session.execute(sql2, {"category": category, "user_id": user_id})
                    for result in results:
                        newlist.append(result[0], result[1], "Edullinen")
            if "Kallis" in prices:
                for category in categories:
                    sql = "SELECT name, category FROM actions WHERE category=:category AND highcost=TRUE UNION SELECT name, category FROM private_actions WHERE category=:category AND highcost=TRUE and creator_id=:user_id"
                    sql2 = text(sql)
                    results = db.session.execute(sql2, {"category": category, "user_id": user_id})
                    for result in results:
                        newlist.append(result[0], result[1], "Kallis")
            return render_template("activity_list.html",results=newlist)
            
            
        #return render_template("activity_list.html", prices = prices, categories = categories)
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


@app.route("/review/<name>", methods=["GET"])
def review(name):
    if request.method == "GET":
        return render_template("review.html", name=name)
    #activity_name = name
    #review = request.form["effects"]
    #if review == 1:
        #effects.add_review(activity_name, True, False, False)
    #elif review == 2:
        #effects.add_review(activity_name, False, True, False)
    #else:
        #effects.add_review(activity_name, False, False, True)
    #return render_template("effects.html")

@app.route("/moods", methods=["GET","POST"])
def mood():
    if request.method == "GET":
        return render_template("moods.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        user_id = session["user_id"]
        feeling = request.form["mood"]
        sent_at2 = datetime.now()
        sent_at = sent_at2.replace(microsecond=0)
        sql = "INSERT INTO moods (feeling, user_id, sent_at) VALUES (:feeling, :user_id, :sent_at)"
        sql2 = text(sql)
        db.session.execute(sql2, {"feeling": feeling, "user_id": user_id, "sent_at": sent_at})
        db.session.commit()
        return redirect("/")

@app.route("/moodlists")
def show_moods():
    user_id = session["user_id"]
    sql = "SELECT feeling, sent_at FROM moods WHERE user_id=:user_id"
    sql2 = text(sql)
    results = db.session.execute(sql2, {"user_id": user_id}).fetchall()
    print(results)
    return render_template("moodlists.html", results = results)

@app.route("/showall")
def showall():
    user_id = session["user_id"]
    sql = "SELECT name, category, free, lowcost, highcost FROM actions UNION SELECT name, category, free, lowcost, highcost FROM private_actions WHERE creator_id=:user_id"
    sql2 = text(sql)
    results = db.session.execute(sql2, {"user_id":user_id}).fetchall()
    newlist = []
    for result in results:
        if result[2] == True:
            cost = "Ilmainen"
        if result[3] == True:
            cost = "Edullinen"
        if result[4] == True:
            cost = "Kallis"
        newlist.append((result[0], result[1], cost))
    return render_template("showall.html",results=newlist)

@app.route("/activity_list", methods=["POST"])
def activity_list():
    user_id = session["user_id"]
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    valinta = request.form["valinta"]
    prices = request.form.getlist("price")
    print(prices)
    categories = request.form.getlist("category")
    if len(prices)==0 or len(categories)==0:
        return render_template("error.html", message="sinä höpsöliini et valinnut tarvittavaa määrää kriteerejä")
    print(categories)
    newlist = []
    if "Ilmainen" in prices:
        for category in categories:
            sql = "SELECT name, category FROM actions WHERE category=:category AND free=TRUE UNION SELECT name, category FROM private_actions WHERE category=:category AND free=TRUE AND creator_id=:user_id"
            sql2 = text(sql)
            results = db.session.execute(sql2, {"category": category, "user_id": user_id})
            for result in results:
                newlist.append((result[0], result[1], "Ilmainen"))
    if "Edullinen" in prices:
        for category in categories:
            sql = "SELECT name, category FROM actions WHERE category=:category AND lowcost=TRUE UNION SELECT name, category FROM private_actions WHERE category=:category AND lowcost=TRUE AND creator_id=:user_id"
            sql2 = text(sql)
            results = db.session.execute(sql2, {"category": category, "user_id": user_id})
            for result in results:
                newlist.append((result[0], result[1], "Edullinen"))
    if "Kallis" in prices:
        for category in categories:
            sql = "SELECT name, category FROM actions WHERE category=:category AND highcost=TRUE UNION SELECT name, category FROM private_actions WHERE category=:category AND highcost=TRUE AND creator_id=:user_id"
            sql2 = text(sql)
            results = db.session.execute(sql2, {"category": category, "user_id": user_id})
            for result in results:
                newlist.append((result[0], result[1], "Kallis"))
    print(newlist)
    if valinta == "decide":
        return render_template("activity_list.html",results=newlist)
    if valinta == "random":
        lenlist = len(newlist)
        if lenlist > 1:
            random_number = randint(0, lenlist-1)
        else:
            random_number = 0
        result = newlist[random_number]
        name = result[0]
        sql = "SELECT category, free, lowcost, highcost FROM actions WHERE name = :name UNION SELECT category, free, lowcost, highcost FROM private_actions WHERE name = :name"
        sql2 = text(sql)
        result = db.session.execute(sql2, {"name": name}).fetchone()
        if result[1] == True:
            price = "Ilmainen"
        elif result[2] == True:
            price = "Edullinen"
        else:
            price = "Kallis"
        return render_template("activity.html", name = name, category = result[0], price=price)
        


@app.route("/random")
def randomize():
    sql = "SELECT name, category, free, lowcost, highcost FROM actions"
    sql2 = text(sql)
    results = db.session.execute(sql2).fetchall()
    newlist = []
    for result in results:
        if result[2] == True:
            cost = "Ilmainen"
        if result[3] == True:
            cost = "Edullinen"
        if result[4] == True:
            cost = "Kallis"
        newlist.append((result[0], result[1], cost))
    lenlist = len(newlist)
    if lenlist > 1:
        random_number = randint(0,lenlist-1)
    else:
        random_number = 0
    print(random_number)
    print(newlist)
    result = newlist[random_number]
    name = result[0]
    category = result[1]
    price = result[2]
    print(name)
    print(category)
    print(price)
    return render_template("activity.html", name = name, category = category, price=price)


@app.route("/activity/<name>")
def chosen_activity(name):
    user_id = session["user_id"]
    sql = "SELECT category, free, lowcost, highcost FROM actions WHERE name = :name UNION SELECT category, free, lowcost, highcost FROM private_actions WHERE name = :name AND creator_id = :user_id"
    sql2 = text(sql)
    result = db.session.execute(sql2, {"name": name, "user_id": user_id}).fetchone()
    category = result[0]
    if result[1] == True:
        price = "Ilmainen"
    if result[2] == True:
        price = "Edullinen"
    if result[3] == True:
        price = "Kallis"

    return render_template("activity.html", name = name, category = category, price=price)


@app.route("/effects/<name>", methods = ["GET", "POST"])
def effects(name):
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        effect = request.form["effects"]
        low = False
        neutral = False
        high = False
        if effect == "1":
            low = True
        if effect == "2":
            neutral = True
        if effect == "3":
            high = True
        sql = "INSERT INTO effects (action_name, low, neutral, high) VALUES (:action_name, :low, :neutral, :high)"
        sql2 = text(sql)
        db.session.execute(sql2, {"action_name":name, "low":low, "neutral":neutral, "high":high})
        db.session.commit()
        return redirect("/effect")
    if request.method == "GET":
        return render_template("effect.html")

@app.route("/effect")
def effect():
    return render_template("effect.html")

@app.route("/all_effects", methods=["GET","POST"])
def all_effects():
    user_id = session["user_id"]
    if request.method == "GET":
        results = show_reviews(user_id)
        return render_template("all_effects.html", results = results)
    if request.method == "POST":
        user_id = session["user_id"]
        categories = request.form.getlist("category")
        prices = request.form.getlist("price")
        criteria = request.form["criteria"]
        results = filter_reviews(categories, prices, criteria, user_id)
        return render_template("all_effects.html", results = results)
    
