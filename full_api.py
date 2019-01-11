
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# python3 interpreter > import db from file > db.create_all()
# to configure db and initiate models (below)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flask_api'
db = SQLAlchemy(app)


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
        owner_id = language['owner_id']

        # creates a new model object, stores it in db, and persists it
        new_language = Language(name=name, framework=framework, owner_id=owner_id)
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


@app.route('/user/signup', methods=['POST'])
def signup():
    user = request.get_json()

    new_user = User(username=user['username'], email=user['email'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': '201'})


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404)

    return jsonify(user.to_json())


# runs the app if launched from cmd line, should not be used in production
if __name__ == '__main__':
    app.run(debug=True, port=8080)

