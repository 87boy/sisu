#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import *

# Create the Flask-Restless API manager.
api_manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
api_manager.create_api(User, collection_name='user', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)
api_manager.create_api(Building, collection_name='building', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)
api_manager.create_api(Floor, collection_name='floor', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)
api_manager.create_api(Room, collection_name='room', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)
api_manager.create_api(Device, collection_name='device', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)
api_manager.create_api(Sensor, collection_name='sensor', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)
api_manager.create_api(SensorData, collection_name='sensor_data', methods=[
                       'GET', 'POST', 'DELETE', 'PATCH', 'PUT'], url_prefix='/api/v1', allow_patch_many=True)

# start the flask loop
app.run()
