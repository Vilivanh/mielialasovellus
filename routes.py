from app import app
from flask import render_template, request, redirect
import users
from users import register, login




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
        if not users.register(username, pass1):
            return render_template("error.html", message = "rekisteröinti epäonnistui")
        return redirect("/")



