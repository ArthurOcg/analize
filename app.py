from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    response = {
        "data": "Hello World!"
        }
    return jsonify(response), 200

@app.route('/oi', methods=['GET'])
def comecando():
    return {"Só vai assim!"}, 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
