
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# python3 interpreter > import db from file > db.create_all()
# to configure db and initiate models (below)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flask_api'
db = SQLAlchemy(app)


# models for ORM
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
"""


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


# handles creating and getting all
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        language = request.get_json()

        for key, value in language.items():
            # returns psuedo 403 if a field is blank
            if not value:
                return jsonify({'error': 'bad request'})

        # sets local variables from request
        name = language['name']
        framework = language['framework']

        # creates a new model object, stores it in db, and persists it
        new_language = Language(name=name, framework=framework)
        db.session.add(new_language)
        db.session.commit()

        return jsonify({'status': '201'})

    elif request.method == 'GET':
        languages = Language.query.all()
        # returns custom formatted objects from the query
        return jsonify({'languages': [language.to_json() for language in languages]})

    # if method is not GET/POST
    else:
        return jsonify({'status': 'method not supported'})


# handles all requests that require an object id
@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def action_by_id(id):

    if request.method == 'GET':
        language = Language.query.filter_by(id=id).first()
        if not language:
            return jsonify({'status': 'bad request'})
        return jsonify(language.to_json())

    elif request.method == 'PUT':
        # grabs language by id
        language = Language.query.get(id)
        if not language:
            return jsonify({'status': 'Entry does not exist'})

        # get request values and change object values
        update_lang = request.get_json()
        language.name = update_lang['name']
        language.framework = update_lang['framework']

        # saves database
        db.session.merge(language)
        db.session.commit()
        return jsonify({'status': '204'})

    elif request.method == 'DELETE':
        language = Language.query.get(id)
        if not language:
            # aborts and returns a 404 if language doesnt exist
            abort(404)
        db.session.delete(language)
        db.session.commit()
        return jsonify({'status': '204'})

    else:
        # flask handles this automatically, but why not have it for logics sake
        return jsonify({'status': 'Method not supported'})


# runs the app if launched from cmd line, should not be used in production
if __name__ == '__main__':
    app.run(debug=True, port=8080)

