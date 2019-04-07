import hashlib

from . import app, db
from flask import render_template, g, redirect, url_for, request, jsonify
import json

from .models import *


@app.route('/api/login', methods=['POST'])
def api_login():
    return jsonify({'name': 'Chris'})


@app.route('/login', methods=['POST', 'GET'])
def login():
    f = open('text.txt', 'r')
    for line in f:
        if (line.split()[0] == request.post[username] and line.split()[1] == request.post[password]):
            return render_template('mainpage.html')        
    return render_template('loginpage.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    f = open('text.txt', 'a')
    f.write(request.post[username] + ' ' + request.post[password] + ' ' + request.post[name] + '\n')
    return render_template('mainpage.html')
