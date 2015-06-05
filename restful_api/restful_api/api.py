#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask.ext.restful import abort, Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy

# from config import *
from model import *

api = Api(app)

# stdlib
# from json import dumps

def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object. """
    json = {}
    # json['fields'] = {}
    # json['pk'] = getattr(model, 'id')
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        # json['fields'][col.name] = getattr(model, col.name)
        json[col.name] = getattr(model, col.name)
    # return dumps([json])
    return json

def to_json_list(model_list):
    json_list = []
    for model in model_list:
        json_list.append(to_json(model))
    return json_list

class UserResource(Resource):

    def get(self, user_id):
        record = User.query.filter_by(id=user_id).first_or_404()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        record = User.query.filter_by(id=user_id).first()
        if record:
            record.password = args['password']
        result = db.session.commit()
        # return args, 201
        return to_json(record), 201


class UserList(Resource):

    def get(self):
        user_list = User.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(user_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        new_user = User(args['username'], args['password'], args['email'])
        db.session.add(new_user)
        result = db.session.commit()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        return result, 201

class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and (args['password'] == user.password):
            return {'status':'login successed'}, 200
        else:
            return {'status':'login failed'}, 200


api.add_resource(UserList, '/user', '/user/')
api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(Login, '/login', '/login/')


if __name__ == '__main__':
    app.run()
