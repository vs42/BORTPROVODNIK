import hashlib

from . import app, db
from flask import render_template, g, redirect, url_for, request, jsonify
import json

from requests.compat import basestring

from .models import *

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


@app.route('/api/login', methods=['POST'])
def api_login():
    return jsonify({'name': 'Chris'})

@app.route('/login')
def login():
