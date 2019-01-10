
from flask import Flask, jsonify, request

app = Flask(__name__)

languages = [{'name': 'Python'}]


@app.route('/lang/<name>', methods=['PUT'])
def edit(name):
    lang = [language for language in languages if langage['name'] == name]
    lang['name'] = request.json['name']
    return jsonify({'langugage': lang})


if __name__ == '__main__':
    app.run(debug=True, port=8080)

