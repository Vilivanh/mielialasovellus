from flask import Flask
from os import getenv

moodapp = Flask(__name__)
moodapp.secret_key = getenv("SECRET_KEY")

import routes
