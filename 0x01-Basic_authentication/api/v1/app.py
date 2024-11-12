#!/usr/bin/env python3
""" Main application module """

from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
CORS(app)

auth = None
AUTH_TYPE = os.getenv('AUTH_TYPE', 'auth')
if AUTH_TYPE == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()

@app.before_request
def before_request():
    """ Method that runs before each request """
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)

@app.errorhandler(401)
def unauthorized_error(error):
    """ Unauthorized error handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden_error(error):
    """ Forbidden error handler """
    return jsonify({"error": "Forbidden"}), 403

@app.route('/api/v1/status', methods=['GET'])
def status():
    """ Status endpoint """
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv('API_PORT', 5000)))

