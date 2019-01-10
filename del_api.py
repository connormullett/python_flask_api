
from flask import Flask, jsonify, request

app = Flask(__name__)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}, {'name': 'Ruby'}]


@app.route('/lang/<string:name>', methods=['DELETE'])
def delete(name):
    langs = [language for language in languages if language['name'] == name]
    try:
        languages.remove(langs[0])
    except Exception:
        return jsonify({'status': '404'})

    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, port=8080)

