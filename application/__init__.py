from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
session = Session()
login_manager = LoginManager()

# function to create the flask application
def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')

    # db plugin
    db.init_app(app)
    # session plugin
    session.init_app(app)
    # login plugin
    login_manager.init_app(app)

    with app.app_context():
        # Application Routes
        #from . import routes, user, stocks
        from . import user, stock, main

        db.create_all()

        # Application Blueprints
        app.register_blueprint(user.user_bp)
        app.register_blueprint(stock.stock_bp)

        return app
