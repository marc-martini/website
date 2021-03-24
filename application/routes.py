from flask import current_app as app
from flask import request, render_template, make_response
from .db_models import db, db_User

@app.route("/")
def home():
    return "Hello World!"


