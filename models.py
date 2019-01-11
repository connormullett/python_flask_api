
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
        BadSignature, SignatureExpired)

from full_api import db, app


# models for ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_json(self):
        return {
                'username': self.username,
                'email': self.email
                }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # only used in user registration
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    framework = db.Column(db.String(10), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, framework, owner_id):
        self.name = name
        self.framework = framework
        self.owner_id = owner_id

    def to_json(self):
        return {
                'name': self.name,
                'framework': self.framework,
                # queries for the owner_id given, grabs the object,
                # and calls to_json() on user object
                'posted_by': User.query.filter_by(id=self.owner_id).all().to_json()
                }

