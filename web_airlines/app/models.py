from . import db, app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128))

    def generate_auth_token(self, expiration=600000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class ConsignmentNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flightNumber = db.Column(db.String(128))
    data = db.Column(db.String(128), unique=True)
    date = db.Column(db.Integer)
    airplaneNumber = db.Column(db.String(128))
    signature = db.Column(db.String(128))

    signed_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Act(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flightNumber = db.Column(db.String(128))
    data = db.Column(db.String(128), unique=True)
    date = db.Column(db.Integer)
    airplaneNumber = db.Column(db.String(128))
    signature = db.Column(db.String(128))

    signed_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class FlightAttendant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.String(128), unique=True, index=True)
    name = db.Column(db.String(128))
