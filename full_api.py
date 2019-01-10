
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# python3 interpreter > import db from file > db.create_all()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flask_api'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    framework = db.Column(db.String(10), unique=True)

    def __init__(self, name, framework):
        self.name = name
        self.framework = framework

    def to_json(self):
        return {
                'name': self.name,
                'framework': self.framework
                }


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language = request.get_json()

        for key, value in language.items():
            if not value:
                return jsonify({'error': 'bad request'})

        name = language['name']
        framework = language['framework']

        new_language = Language(name=name, framework=framework)
        db.session.add(new_language)
        db.session.commit()

        return jsonify({'status': '201'})

    elif request.method == 'GET':
        languages = Language.query.all()
        return jsonify({'languages': [language.to_json() for language in languages]})

    else:
        return jsonify({'status': 'method not supported'})


@app.route('/<id>')
def detail(id):
    pass


@app.route('/<id>', methods=['PUT'])
def update(id):
    pass


@app.route('/<id>')
def delete(id):
    pass


if __name__ == '__main__':
    app.run(debug=True, port=8080)

