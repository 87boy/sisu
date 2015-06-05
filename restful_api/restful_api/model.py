#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config.from_object(rest_api.default_settings)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)

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

class Floor(db.Model):
    __tablename__ = 'floor'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    building_id = db.Column(
        db.Integer, db.ForeignKey('building.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship('Room', backref='floor', lazy='dynamic')


class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    floor_id = db.Column(db.Integer, db.ForeignKey('floor.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship('Device', backref='room', lazy='dynamic')


class Device(db.Model):
    __tablename__ = 'device'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship(
        'SensorData', backref='device', lazy='dynamic')


class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    relationship = db.relationship(
        'SensorData', backref='sensor', lazy='dynamic')


class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    sensor_id = db.Column(
        db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    device_id = db.Column(
        db.Integer, db.ForeignKey('device.id'), nullable=False)
    value = db.Column(db.Float)
    datetime = db.Column(db.DateTime)
    status = db.Column(db.Integer)

# Create the database tables.
# db.create_all()
