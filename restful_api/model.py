#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config.from_object(rest_api.default_settings)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
