from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    # def __repr__(self):
    #     return '<User %r>' % self.username

# from my_sqlalchemy import db
# db.create_all()
# from my_sqlalchemy import User
# admin = User('admin', 'admin@example.com')
# guest = User('guest', 'guest@example.com')
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()
# users = User.query.all()
# print users
# print type(users)
# import json
# print json.dumps(users)