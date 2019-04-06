from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, template_folder='template', static_folder='static')
CORS(app)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, models