#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask.ext.restless

from config import *

# Create the Flask application and the Flask-SQLAlchemy object.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

# Create your Flask-SQLALchemy models as usual but with the following two
# (reasonable) restrictions:
#   1. They must have a primary key column of type sqlalchemy.Integer or
#      type sqlalchemy.Unicode.
#   2. They must have an __init__ method which accepts keyword arguments for
#      all columns (the constructor in flask.ext.sqlalchemy.SQLAlchemy.Model
#      supplies such a method, so you don't need to declare a new one).


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


class Building(db.Model):
    __tablename__ = 'building'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    latitude = db.Column(db.String(255))
    longitude = db.Column(db.String(255))
    description = db.Column(db.String(255))


class Floor(db.Model):
    __tablename__ = 'floor'

    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    floor_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))


class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    description = db.Column(db.String(255))


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer)
    value = db.Column(db.Float)
    datetime = db.Column(db.DateTime)
    status = db.Column(db.Integer)

# Create the database tables.
# db.create_all()
