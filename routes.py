from app import app
from flask import render_template, request, redirect, session
import users
from users import register, login
from sqlalchemy.sql import text
from choose import showall, random, decide


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"]=username
        if not users.login(username, password):
            return render_template("error.html", message="virheellinen kirjautumisyritys")
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
        return redirect("/")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create", methods=["POST"])
def create():
    nimi = request.form["nimi"]
    kategoria = request.form["kategoria"]
    hinta = request.form["hinta"]
    return render_template("create.html", nimi=nimi, kategoria=kategoria, hinta=hinta)

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
        categories = request.form.getlist("kategoria")
        prices = request.form.getlist("kustannus")
        valinta = request.form["valinta"]
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
            chosen == decide(categories, free, lowcost, highcost)  
            return render_template(chosen, "activity.html")
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
            chosen == random(categories, free, lowcost, highcost)
            return render_template(chosen, "activity.html")


#@app.route("/review/<text:name>", methods=["POST"])
#def review(name):
    #activity_name = name
   # review = request.form["effect"]
    #if review == 1:
     #   effects.add_review(activity_name, True, False, False)
    #elif review == 2:
     #   effects.add_review(activity_name, False, True, False)
    #else:
     #   effects.add_review(activity_name, False, False, True)
    #return render_template("effects.html")

    
    
