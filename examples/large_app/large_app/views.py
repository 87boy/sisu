#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_api import app

@app.route('/')
def index():
    return 'Hello World!'
