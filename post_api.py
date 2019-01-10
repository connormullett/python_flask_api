
from flask import Flask, jsonify, request

app = Flask(__name__)

languages = [{'name': 'JavaScript'}, {'name': 'Python'}]

@app.route('/lang/', methods=['POST'])
def create_language():
    language = {'name': request.json['name']}

    languages.append(language)
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, port=8080)

