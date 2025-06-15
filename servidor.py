from flask import Flask, jsonify
from waitress import serve
from dotenv import load_dotenv

from modelo_treinado.modelo_treinado import download_model
from routes.analise import analise as analise_route_logic 

print('Iniciando variáveis de ambiente...')
load_dotenv()

print('Downloading e carregando o modelo treinado...')

download_model()

app = Flask(__name__)

@app.route('/teste', methods=['GET'])
def testeConexao():
    print('Conectado com sucesso!')
    return jsonify({"message": "Conexão bem-sucedida!", "status_code": 200}), 200

@app.route('/analise', methods=['POST'])
def analise_endpoint(*args, **kwargs):
    return analise_route_logic(*args, **kwargs)

if __name__ == '__main__':
    print('Servidor Flask iniciado na porta 5001...')
    serve(app, host='0.0.0.0', port=5001)