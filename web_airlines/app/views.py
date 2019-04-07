import hashlib

from . import app, db
from flask import render_template, g, redirect, url_for, request, jsonify
import json
import rsa
import requests
from .models import *


@app.route('/api/login', methods=['POST'])
def api_login():
    public = request.json['publicKey']
    private = request.json['privateKey']
    name = request.json['name']
    s = 'abc'
    #if rsa.decrypt(rsa.encrypt(s, private), public) != s:
    #    return jsonify({'error': 'invalid keys'})
    user = FlightAttendant(public_key=public, name=name)
    db.session.add(user)
    db.session.commit()
    requests.request(method='POST', url=app.config['SUPPLY_URL'],
                     data={'public':public, 'name':name, 'id':user.id, 'code':app.config['SECRET_KEY']})
    return jsonify({'name': name, 'id': str(user.id)})


@app.route('/api/push_note', methods=['POST'])
def push_note():
    sign = request.json['sign']
    signed_by = int(request.json['signedBy'])
    data = request.json['data']
    flightNumber = request.json['flightNumber']
    date = request.json['date']
    airplaneNumber = request.json['airplaneNumber']
    with open('Files\\' + sign, 'w', encoding='utf-8') as file:
        file.write(data)
    note = ConsignmentNote(sign=sign, signed_by=signed_by, data=sign, date=date, flightNumber=flightNumber, airplaneNumber=airplaneNumber)
    db.session.add(note)
    db.session.commit()
    return 'OK'


@app.route('/api/push_act', methods=['POST'])
def push_act():
    sign = request.json['sign']
    signed_by = int(request.json['signedBy'])
    data = request.json['data']
    flightNumber = request.json['flightNumber']
    date = request.json['date']
    airplaneNumber = request.json['airplaneNumber']
    with open('Files\\' + sign, 'w', encoding='utf-8') as file:
        file.write(data)
    act = Act(sign=sign, signed_by=signed_by, data=sign, date=date, flightNumber=flightNumber, airplaneNumber=airplaneNumber)
    db.session.add(act)
    db.session.commit()

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('loginpage.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('mainpage.html')
