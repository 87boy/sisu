#!/usr/bin/env python
# -*- coding: utf-8 -*-

activate_this = '/home/ubuntu/virtual_env/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/home/ubuntu/git/sisu/restless_api/")

from restless_api import app as application
#application.secret_key = 'test'

