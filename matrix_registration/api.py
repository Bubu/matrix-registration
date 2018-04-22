from flask import Flask, abort, jsonify, request

import hashlib
import hmac
import yaml
import requests
import sys

from .synapse_register import create_account 
from .config import Config 


app = Flask(__name__)

SHARED_SECRET = Config['SHARED_SECRET']
SERVER_LOCATION = Config['SERVER_LOCATION']


@app.route('/register', methods=['POST'])
def register():
    app.logger.debug('an account registration was requested...')
    if all(req in request.form for req in ('username', 'password')):
        username = request.form['username'].rsplit(":")[0].split("@")[-1]
        password = request.form['password']
        if username and password:
            app.logger.debug('creating account %s...' % username)
            try:
                account_data = create_account(username,
                                              password,
                                              SERVER_LOCATION,
                                              SHARED_SECRET)
            except requests.exceptions.HTTPError as e:
                app.logger.warning(e)
                abort(400)
            app.logger.debug('account creation succeded!')
            return jsonify(account_data)
    app.logger.debug('account creation failed!')
    abort(400)
