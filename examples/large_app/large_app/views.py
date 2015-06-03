#!/usr/bin/env python
# -*- coding: utf-8 -*-

from large_app import app

@app.route('/')
def index():
    return 'Hello World!'
