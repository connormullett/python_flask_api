
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import models

# python3 interpreter > import db from file > db.create_all()
# to configure db and initiate models (located in models.py)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/flask_api'
app.config['SECRET_KEY'] = 'ThisIsASecretKey'

db = SQLAlchemy(app)


# handles creating and getting all
# login required
"""params
token: string
owner_id: int
name: string
framework: string
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        token = request.get_json()['token']

        if not token:
            return {'status': '401 unauthorized'}

        # new
        # TODO: Need to grab user object from owner_id
        owner_id = request.get_json()['owner_id']
        user = models.User.query.get(owner_id)

        if not user.verify_auth_token(token):
            return {'status': '401 invalid token'}
        # end new

        language = request.get_json()

        # sets local variables from request
        name = language['name']
        framework = language['framework']
        owner_id = language['owner_id']

        # creates a new model object, stores it in db, and persists it
        new_language = models.Language(name=name, framework=framework, owner_id=owner_id)
        db.session.add(new_language)
        db.session.commit()

        return jsonify({'status': '201'})

    elif request.method == 'GET':
        languages = models.Language.query.all()
        # returns custom formatted objects from the query
        return jsonify({'languages': [language.to_json() for language in languages]})

    # if method is not GET/POST
    else:
        return jsonify({'status': 'method not supported'})


# handles all requests that require an object id
@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def action_by_id(id):

    if request.method == 'GET':
        language = models.Language.query.filter_by(id=id).first()

        if not language:
            return jsonify({'status': 'bad request'})

        return jsonify(language.to_json())

    elif request.method == 'PUT':
        # grabs language by id
        language = models.Language.query.get(id)

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
        language = models.Language.query.get(id)

        if not language:
            return jsonify({'status': '404'})

        db.session.delete(language)
        db.session.commit()
        return jsonify({'status': '204'})

    else:
        # flask handles this automatically, but why not have it for logics sake
        return jsonify({'status': 'Method not supported'})


"""params
username: string
email: string
password: string
verify_password: string
"""
@app.route('/user/signup', methods=['POST'])
def signup():
    # grab json
    user = request.get_json()

    # verify request and password matching
    if not user['password'] or not user['verify_password']:
        return jsonify({'status': '403'})

    if user['password'] != user['verify_password']:
        return jsonify({'status': 'password mismatch'})

    # create new user
    new_user = models.User(username=user['username'], email=user['email'])
    new_user.hash_password(user['password'])

    # save user
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': '201'})


@app.route('/logout', methods=['POST'])
def logout():
    pass


@app.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
def user_specific(id):

    if request.method == 'GET':
        user = models.User.query.get(id)

        if not user:
            return jsonify({'status': '404'})

        return jsonify(user.to_json())

    elif request.method == 'PUT':
        user = models.User.query.get(id)

        if not user:
            return jsonify({'status': '404'})

        update_user = request.get_json()
        user.email = update_user['email']
        user.username = update_user['username']

        db.session.merge(user)
        db.session.commit()
        return jsonify({'status': '204'})

    elif request.method == 'DELETE':
        user = models.User.query.get(id)

        if not user:
            return jsonify({'status': '404'})

        db.session.delete(user)
        db.commit()
        db.commit

        return jsonify({'status': '204'})


"""params
username: string
password: string
"""
@app.route('/token', methods=['POST'])
def get_auth_token():
    username = request.get_json()['username']
    password = request.get_json()['password']

    user = models.User.query.filter_by(username=username).first()

    if user.verify_password(password) is True:
        token = user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})

    return jsonify({'status': '403'})


@app.route('/user', methods=['GET'])
def get_users():
    users = models.User.query.all()


# runs the app if launched from cmd line, should not be used in production
if __name__ == '__main__':
    app.run(debug=True, port=8080)

