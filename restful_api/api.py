#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask.ext.restful import abort, Api, Resource, reqparse
from flask.ext.sqlalchemy import SQLAlchemy

#from config import *
from model import *

api = Api(app)


class UserResource(Resource):

    def get(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        return jsonify(json_list=result), 200

    def put(self, user_id):
        args = parser.parse_args()
        return args, 201


class UserList(Resource):

    def get(self):
        result = User.query.all()
        return jsonify(json_list=[i.serialize for i in result]), 200

    def post(self):
        args = parser.parse_args()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        return args, 201

api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(UserList, '/user/')

if __name__ == '__main__':
    app.run(debug=True)
