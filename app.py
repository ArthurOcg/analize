from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello')
def hello():
    response = {
        "data": "Hello World!"
        }
    return jsonify(response), 200

@app.route('/oi')
def comecando():
    return "Só vai assim!"

app.run(debug=True, use_reloader=True)