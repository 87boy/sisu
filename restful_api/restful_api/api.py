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

# import json
# from sqlalchemy.ext.declarative import DeclarativeMeta
# class AlchemyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields

#         return json.JSONEncoder.default(self, obj)

#     def new_alchemy_encoder():
#         _visited_objs = []
#         class AlchemyEncoder(json.JSONEncoder):
#             def default(self, obj):
#                 if isinstance(obj.__class__, DeclarativeMeta):
#                     # don't re-visit self
#                     if obj in _visited_objs:
#                         return None
#                     _visited_objs.append(obj)

#                     # an SQLAlchemy class
#                     fields = {}
#                     for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                         fields[field] = obj.__getattribute__(field)
#                     # a json-encodable dict
#                     return fields

#                 return json.JSONEncoder.default(self, obj)
#         return AlchemyEncoder

# #c = Floor()
# #print json.dumps(c, cls=AlchemyEncoder)
# print json.dumps(e, cls=new_alchemy_encoder(), check_circular=False)

class UserResource(Resource):

    def get(self, user_id):
        record = User.query.filter_by(id=user_id).first()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        args = parser.parse_args(strict=True)
        record = User.query.filter_by(id=user_id).first()
        if record:
            record.password = args['password']
        db.session.commit()
        # return args, 201
        return to_json(record), 201

    def delete(self, user_id):
        record = User.query.filter_by(id=user_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class UserList(Resource):

    def get(self):
        record_list = User.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(record_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args(strict=True)
        new_record = User(args['username'], args['password'], args['email'])
        db.session.add(new_record)
        result = db.session.commit()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        return new_record.id, 201


class Login(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and (args['password'] == user.password):
            return {'status': 'login successed'}, 200
        else:
            return {'status': 'login failed'}, 200


class BuildingResource(Resource):

    def get(self, building_id):
        record = Building.query.filter_by(id=building_id).first()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, building_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        args = parser.parse_args(strict=True)
        record = Building.query.filter_by(id=building_id).first()
        if record:
            record.name = args['name']
        db.session.commit()
        # return args, 201
        return to_json(record), 201

    def delete(self, building_id):
        record = Building.query.filter_by(id=building_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class BuildingList(Resource):

    def get(self):
        building_list = Building.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(building_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        parser.add_argument('latitude', type=str)
        parser.add_argument('longitude', type=str)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        new_record = Building(args['name'], args['latitude'], args['longitude'], args['description'])
        db.session.add(new_record)
        result = db.session.commit()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        return new_record.id, 201


class FloorResource(Resource):

    def get(self, floor_id):
        record = Floor.query.filter_by(id=floor_id).first()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, floor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        args = parser.parse_args()
        record = Floor.query.filter_by(id=floor_id).first()
        if record:
            record.name = args['name']
        db.session.commit()
        # return args, 201
        return to_json(record), 201

    def delete(self, floor_id):
        record = Floor.query.filter_by(id=floor_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class FloorList(Resource):

    def get(self):
        floor_list = Floor.query.all()
        # return jsonify(json_list=[i.serialize for i in user_list]), 200
        # results = []
        # for idx in user_list:
        #     results.append(to_json(idx))
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('building_id', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        new_record = Floor(args['building_id'], args['name'], args['description'])
        db.session.add(new_record)
        result = db.session.commit()
        # new_user = User(username, password, email)
        # db.session.add(new_user)
        # result = db.session.commit()
        return new_record.id, 201


class RoomResource(Resource):

    def get(self, room_id):
        record = Room.query.filter_by(id=room_id).first()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, room_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        record = Room.query.filter_by(id=room_id).first()
        if record:
            record.name = args['name']
            db.session.commit()
            return {'status': 'updated'}, 201
        else:
            return {'status': 'room not exit'}, 404

    def delete(self, room_id):
        record = Room.query.filter_by(id=room_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class RoomList(Resource):

    def get(self):
        floor_list = Room.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('floor_id', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        new_record = Room(
            args['floor_id'], args['name'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


class DeviceResource(Resource):

    def get(self, device_id):
        record = Device.query.filter_by(id=device_id).first()
        if record is not None:
            return to_json(record), 200
        else:
            return {'status': 'device not exit'}

    def put(self, device_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=unicode)
        args = parser.parse_args()
        record = Device.query.filter_by(id=device_id).first()
        if record:
            record.name = args['name']
        db.session.commit()
        return to_json(record), 201

    def delete(self, device_id):
        record = Device.query.filter_by(id=device_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class DeviceList(Resource):

    def get(self):
        floor_list = Device.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('room_id', type=int)
        parser.add_argument('name', type=unicode)
        parser.add_argument('description', type=unicode)
        parser.add_argument('uuid', type=str)
        args = parser.parse_args(strict=True)
        new_record = Device(
            args['room_id'], args['name'],
            args['uuid'], args['description'])
        db.session.add(new_record)
        result = db.session.commit()
        return new_record.id, 201


class sensorResource(Resource):

    def get(self, sensor_id):
        record = Sensor.query.filter_by(id=sensor_id).first()
        if record is not None:
            return to_json(record), 200
        else:
            return {"status": "sensor not exit"}

    def put(self, sensor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        record = Sensor.query.filter_by(id=sensor_id).first()
        if record:
            record.name = args['name']
            db.session.commit()
            return to_json(record), 201
        else:
            return {"status": "sensor not exit"}

    def delete(self, sensor_id):
        record = Sensor.query.filter_by(id=sensor_id).first()
        if record is not None:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'deleted'}, 204
        else:
            return {"status": "sensor not exit"}


class sensorList(Resource):

    def get(self):
        floor_list = Sensor.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str, location='json')
        parser.add_argument('name', type=unicode, location='json')
        parser.add_argument('uuid', type=str, location='json')
        parser.add_argument('description', type=unicode, location='json')
        args = parser.parse_args(strict=True)
        new_record = Sensor(
            args['type'], args['name'], args['uuid'], args['description'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


class DataResource(Resource):

    def get(self, data_id):
        record = SensorData.query.filter_by(id=data_id).first()
        # return jsonify(json_list=record), 200
        return to_json(record), 200

    def put(self, data_id):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=str)
        args = parser.parse_args()
        record = SensorData.query.filter_by(id=data_id).first()
        if record:
            record.value = args['value']
            db.session.commit()
            return {"status": "updated"}, 201
        else:
            return {"status": "data not exit"}

    def delete(self, data_id):
        record = SensorData.query.filter_by(id=data_id).first()
        db.session.delete(record)
        db.session.commit()
        return {'status': 'deleted'}, 204


class dList(Resource):

    def get(self):
        floor_list = SensorData.query.all()
        return to_json_list(floor_list), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('device_id', type=int)
        parser.add_argument('sensor_id', type=int)
        parser.add_argument('value', type=unicode)
        parser.add_argument('datetime', type=str)
        parser.add_argument('status', type=int)
        args = parser.parse_args(strict=True)
        new_record = SensorData(
            args['device_id'], args['sensor_id'], args['value'],
            args['datetime'], args['status'])
        db.session.add(new_record)
        db.session.commit()
        return new_record.id, 201


# add a new device


class locationList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        parser.add_argument('device_name', type=str)
        parser.add_argument('description', type=unicode)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first_or_404()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first_or_404()
            print args['room_name']
            print floorInfor.id
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first_or_404()
                if roomInfor:
                    new_record = Device(
                        roomInfor.id, args['device_name'],
                        args['uuid'], args['description'])
                    db.session.add(new_record)
                    db.session.commit()
                return {"status": "insert successful"}, 201
            else:
                return {"error": "floor not exit"}
        else:
            return {"error": "building not exit"}

# lookup, update, delete a device


class locationResource(Resource):

    def get(self, uuid):
        record = Device.query.filter_by(uuid=uuid).first()
        if record:
            try:
                roomInfor = Room.query.filter_by(
                    id=record.room_id).first_or_404()
                floorInfor = Floor.query.filter_by(
                    id=roomInfor.floor_id).first_or_404()
                buildInfor = Building.query.filter_by(
                    id=floorInfor.building_id).first_or_404()
                deviceInfor = {}
                deviceInfor['floor_name'] = floorInfor.name
                deviceInfor['room_name'] = roomInfor.name
                deviceInfor['build_name'] = buildInfor.name
                return deviceInfor, 200
            except:
                return {"warning": "you may input error information,\
                please ask the Administrator"}
        else:
            return {"error": "device not exit"}

    def put(self, uuid):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        args = parser.parse_args()
        record = Device.query.filter_by(uuid=uuid).first()
        if record:
            record.uuid = args['uuid']
            db.session.commit()
            return {"status": 'updated'}, 201
        else:
            return {"status": 'device not exit'}, 404

    def delete(self, uuid):
        record = Device.query.filter_by(uuid=uuid).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            return {'status': 'deleted'}, 204
        else:
            return {'status': 'device not exit'}


class dataSensor(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        parser.add_argument('sensor_type', type=str)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first_or_404()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first_or_404()
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first_or_404()
                if roomInfor:
                    deviceInfor = Device.query.filter_by(
                        room_id=roomInfor.id).first_or_404()
        sensorInfor = Sensor.query.filter_by(
            type=args['sensor_type']).first_or_404()
        if sensorInfor and deviceInfor:
            buf = SensorData.query.filter_by(
                sensor_id=sensorInfor.id,
                device_id=deviceInfor.id
            ).order_by('datetime desc').limit(10)
            if buf is not None:
                return to_json_list(buf), 201
            else:
                return {"status": "no data"}
        else:
            return {"status": "no data"}


class dataList(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('build_name', type=unicode)
        parser.add_argument('floor_name', type=str)
        parser.add_argument('room_name', type=str)
        args = parser.parse_args(strict=True)
        buildInfor = Building.query.filter_by(
            name=args['build_name']).first_or_404()
        if buildInfor:
            floorInfor = Floor.query.filter_by(
                name=args['floor_name'],
                building_id=buildInfor.id).first_or_404()
            if floorInfor:
                roomInfor = Room.query.filter_by(
                    name=args['room_name'],
                    floor_id=floorInfor.id).first_or_404()
                if roomInfor:
                    deviceInfor = Device.query.filter_by(
                        room_id=roomInfor.id).first_or_404()
        if deviceInfor:
            result = SensorData.query.filter_by(
                device_id=deviceInfor.id
            ).order_by('datetime desc').limit(10)
        return to_json_list(result), 201

api.add_resource(UserList, '/user', '/user/')
api.add_resource(UserResource, '/user/<user_id>')
api.add_resource(Login, '/login', '/login/')
api.add_resource(BuildingList, '/building', '/building/')
api.add_resource(BuildingResource, '/building/<building_id>')
api.add_resource(FloorList, '/floor', '/floor/')
api.add_resource(FloorResource, '/floor/<floor_id>')
api.add_resource(RoomList, '/room', '/room/')
api.add_resource(RoomResource, '/room/<room_id>')
api.add_resource(DeviceList, '/device', '/device/')
api.add_resource(DeviceResource, '/device/<device_id>')
api.add_resource(dList, '/data', '/data/')
api.add_resource(DataResource, '/data/<data_id>')
api.add_resource(sensorList, '/sensor', '/sensor/')
api.add_resource(sensorResource, '/sensor/<sensor_id>')
api.add_resource(locationResource, '/location/<uuid>')
api.add_resource(locationList, '/location', '/location/')
api.add_resource(dataSensor, '/type/data', '/type/data/')
api.add_resource(dataList, '/all/data', '/all/data/')

if __name__ == '__main__':
    app.run(debug=True)

