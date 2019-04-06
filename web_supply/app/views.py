import hashlib

from . import app, db
from flask import render_template, g, redirect, url_for, request, jsonify
import json

from requests.compat import basestring

from .models import *

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


@app.route('/api/get_all_consignment_notes_by_id', methods=['POST'])
def get_all_consignment_notes_by_id():
    token = request.json['token']
    id = User.verify_auth_token(token).id
    results = []
    for note in ConsignmentNote.query.filter_by(user_id=id).all():
        with open('Files\\' + note.data, 'r') as data:
            formed = {'id': str(note.id),
                      'flightNumber': note.flightNumber,
                      'data': data.read(),
                      'date': note.date,
                      'airplaneNumber': note.airplaneNumber}
        results.append(formed)
    return json.dumps(results)


@app.route('/api/get_all_keys', methods=['POST'])
def get_all_keys():
    token = request.json['token']
    id = User.verify_auth_token(token).id
    results = []
    for key in Keys.query.all():
        formed = {'id': str(key.id),
                  'public': key.public_key,
                  'name': key.name}
        results.append(formed)
    return json.dumps(results)


@app.route('/api/login', methods=['POST'])
def login():
    print(request.json)
    username = request.json['username']
    password = hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest()
    user = User.query.filter_by(username=username, password=password).first()
    g.user = user
    token = g.user.generate_auth_token()
    print(token)
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/register', methods=['POST'])
def register():
    print(request.json)
    username = request.json['username']
    name = request.json['name']
    password = hashlib.sha256(request.json['password'].encode('utf-8')).hexdigest()
    user = User(username=username, password=password, name=name)
    db.session.add(user)
    db.session.commit()
    g.user = user
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
