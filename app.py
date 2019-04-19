from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import cv2

app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['GET'])
def hello():
    response = {
        "data": "Hello World!"
        }
    return jsonify(response), 200

@app.route('/oi', methods=['GET'])
def comecando():
    return jsonify({"Mensagem": "Só vai assim!"}), 200

@app.route('/ui', methods=['POST']) 
def geraTexto():    
    if request.method == 'POST':
        message = request.get_json()
        return message['imagem'],201

def geraHistograma(imagem):
    
    histB  =  cv2.calcHist([imagem], [0], None , [ 256 ], [ 0 , 255 ])
    histG  =  cv2.calcHist([imagem], [1], None , [ 256 ], [ 0 , 255 ])
    histR  =  cv2.calcHist([imagem], [2], None , [ 256 ], [ 0 , 255 ])

    novaVermelha = []
    for i in range(histR.size):
        for j in range(1):
            novaVermelha.append(int(histR[i][j]))

    novaAzul = []
    for i in range(histB.size):
        for j in range(1):
            novaAzul.append(int(histB[i][j]))

    novaVerde = []
    for i in range(histG.size):
        for j in range(1):
            novaVerde.append(int(histG[i][j]))
         
    novaResult = novaVermelha
    novaResult.extend(novaVerde)
    novaResult.extend(novaAzul)
    return novaResult

@app.route('/analize', methods=['POST'])
def read_image():
    if request.method == 'POST':
        header_len = len('data:image/jpeg;base64,')
        image_data = request.json['mensagem'][header_len:];
        #imagem = request.get_json()['mensagem']
        imagem = base64.b64decode(image_data)
        with open('tmp_image.jpg', 'wb') as f:
            f.write(imagem)
            f.close()
        img = cv2.imread('tmp_image.jpg')

        return jsonify({"histograma": geraHistograma(img)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
