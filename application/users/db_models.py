from .. import db
from flask_login import UserMixin

# app user db model

class User(UserMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(100),unique=False, nullable=False)

    lastname = db.Column(db.String(100),unique=False, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    created = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.email)


# user stocks db model

class UserStock(UserMixin, db.Model):

    __tablename__ = 'user_stock'
    id = db.Column(db.Integer, primary_key=True)

    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    symbol = db.Column(db.String(100),unique=True, nullable=False)

    name = db.Column(db.String(300), nullable=False)

    created = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<User {}; Stock {}>'.format(self.userid, self.symbol)
