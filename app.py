from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import cv2
import numpy

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


def recebeImagem(request):
    tamanho_cabeca = len('data:image/jpeg;base64,') #captura tamanho da informacao que sera removida
    image_data = request.json['imagem'][tamanho_cabeca:] #pega a imagem removendo o cabecalho
    print("Pegou imagem do request")
    imagem = base64.b64decode(image_data) #decodifica de base64 para imagem comum
    print("Imagem decodificada")
    with open('tmp_image.jpg', 'wb') as f: #vai gravar a imagem comum no servidor
        f.write(imagem)
        f.close()
    img = cv2.imread('tmp_image.jpg')  #lendo a imagem do servidor
    print("Leu a imagem")
    imagem_de_saida = img.copy()
    print ("Fez a copia")
    cortada = imagem_de_saida[1850:2250, 1350:1750]
    cv2.rectangle(imagem_de_saida, (1850, 2250), (1350, 1750), (0, 255, 0), 8)

    return [cortada, imagem_de_saida, cortada]




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

def encode_image(img):
    ret, data = cv2.imencode('.jpg', img)
    return base64.b64encode(data)

@app.route('/analize', methods=['POST'])
def read_image():
    if request.method == 'POST':
        result = recebeImagem(request)
        corte = result[0]
        sinalizada = result[1]
        shibiu = encode_image(sinalizada)
        histo = geraHistograma(result[2])


        return jsonify({"imagem": 'data:image/jpeg;base64'+ str(shibiu), "histo_cort": histo})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
