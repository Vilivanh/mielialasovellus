from moodapp import moodapp
from flask import render_template, request, redirect

@app.route("/")
def index():
    return "Tervetuloa"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="virheellinen kirjautumisyritys")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        pass1 = request.form["password 1"]
        pass2 = request.form["password 2"]
        if pass1 != pass2:
            return render_template("error.html", message = "salasanat eivät vastaa toisiaan")
        if users.register(username, pass1):
            return redirect("/")
        else:
            return render_template("error.html", message = "rekisteröinti epäonnistui")


