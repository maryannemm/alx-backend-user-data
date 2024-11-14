#!/usr/bin/env python3
""" Views for API endpoints """

from flask import abort
from api.v1.app import app

@app.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized():
    """ Raise a 401 error for unauthorized access """
    abort(401)

@app.route('/api/v1/forbidden', methods=['GET'])
def forbidden():
    """ Raise a 403 error for forbidden access """
    abort(403)

