
from flask import Flask, jsonify, request
app = Flask(__name__)

languages = ({'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'})


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It Works'})


@app.route('/lang', methods=['GET'])
def get_languages():
    return jsonify({'languages': languages})


@app.route('/lang/<name:string>', methods=['GET'])
def get_language(name):
    for language in languages:
        if language['name'] == name:
            return jsonify({'language': language})


if __name__ == '__main__':
    app.run(debug=True, port=8080)

