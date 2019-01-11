
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# models for ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_json(self):
        return {
                'username': self.username,
                'email': self.email
                }


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
                # queries for the owner_id given, grabs the object, and recursively
                # calls to_json()
                'posted_by': User.query.filter_by(id=self.owner_id).first().to_json()
                }

