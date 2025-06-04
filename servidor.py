from flask import Flask, jsonify
from waitress import serve
from dotenv import load_dotenv

from middleware.token import token_necessario
from modelo_treinado.modelo_treinado import download_model
from routes.analise import analise as analise_route_logic 
from routes.cadastro import cadastro as cadastro_route_logic
from routes.login import login as login_route_logic

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
@token_necessario
def analise_endpoint(*args, **kwargs):
    return analise_route_logic(*args, **kwargs)

@app.route('/login', methods=['GET'])
def login_endpoint(*args, **kwargs):
    return login_route_logic(*args, **kwargs)

@app.route('/cadastro', methods=['POST'])
def cadastro_endpoint(*args, **kwargs):
    return cadastro_route_logic(*args, **kwargs)

if __name__ == '__main__':
    print('Servidor Flask iniciado na porta 5000...')
    serve(app, host='0.0.0.0', port=5000)