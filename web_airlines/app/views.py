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
    return render_template('loginpage.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('mainpage.html')
