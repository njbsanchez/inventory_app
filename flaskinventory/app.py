"""initiate flaskinventory"""
from flask import Flask
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "DEV"
app.jinja_env.undefined = StrictUndefined
