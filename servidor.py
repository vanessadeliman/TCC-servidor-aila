from flask import Flask, request, jsonify
from ultralytics import YOLO
import io
from PIL import Image
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from verificacoes import *
from modelos.usuario import *
from functools import wraps

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

app = Flask(__name__)
model = YOLO("modelo-treinado.pt")

# Requisição:
# {
#     "nome": "vanessa", 
#     "email": "vanessa.lima06@aluno.ifce.edu.br",
#     "instituicao": "ifce",
#     "cargo": "estudante"
# }
@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        auth_header = request.headers.get('Authorization')
        email, senha = decode_basic_auth(auth_header)
        body = request.get_json()
        body['email'] = email
        usuario = Usuario.from_json(body)

        db = client['tcc-app-aila']
        collection = db['usuarios']

        # Verificar se o usuário já existe pelo e-mail
        usuario_existente = collection.find_one({"email": email})

        senha = gerar_hash(senha)

        # Se o usuário já existir, atualize o documento. Caso contrário, insira um novo
        if usuario_existente:
            update_result = collection.update_one(
                {"email": email},  # Filtro para encontrar o usuário
                {"$set": {
                    "nome": usuario.nome, 
                    "instituicao": usuario.instituicao,
                    "cargo": usuario.cargo,
                    "senha": senha
                }}
            )
            print(f"Documento atualizado: {update_result.modified_count} documento(s) modificado(s)")
        else:
            document = {
                "nome": usuario.nome, 
                "email": usuario.email, 
                "instituicao": usuario.instituicao,
                "cargo": usuario.cargo,
                "senha": senha
            }
            insert_result = collection.insert_one(document)
            print(f"Documento inserido com ID: {insert_result.inserted_id}")

        usuario_json = usuario.tojson()
        print(f"Usuario JSON: {usuario_json}")

        jwt = criar_jwt(usuario_json)
        return jsonify({"AcessToken": jwt})

    except Exception as e:
        return jsonify({"message": str(e)}), 500

        
@app.route('/login', methods=['GET'])
def login():
    try:
        auth_header = request.headers.get('Authorization')
        email, senha = decode_basic_auth(auth_header)
        
        db = client['tcc-app-aila']
        collection = db['usuarios']
        
        usuario = collection.find_one({"email": email})

        if usuario:
            if verificar_senha(senha, usuario["senha"]):
                usuario_json = {
                    "nome": usuario.get("nome"),
                    "instituicao": usuario.get("instituicao"),
                    "cargo": usuario.get("cargo")
                }
                
                # Gerando o token
                jwt = criar_jwt(usuario_json) 
                usuario_json["AcessToken"] = jwt

                return jsonify(usuario_json), 200
            else:
                return response_with_message("Senha inválida", 401)
        else:
            return response_with_message("Usuário não encontrado", 404)
        
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# Decorador para proteger as rotas
def token_necessario(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token não fornecido"}), 403 
        
        try:
            token = auth_header.split(" ")[1]
            payload = validar_jwt(token)
            request.user_data = payload 
        except Exception as e:
            return jsonify({"message": str(e)}), 401  

        return func(*args, **kwargs) 
    return wrapper

@app.route('/analise', methods=['POST'])
@token_necessario  
def analise():
    # Receber a imagem do cliente
    img_file = request.files['image']
    img_bytes = img_file.read()
    
    # Abrir a imagem com PIL
    img = Image.open(io.BytesIO(img_bytes))
    
    # Realizar a inferência
    results = model(img)
    
    # Acessar os resultados diretamente
    boxes = results[0].boxes.xyxy  # Coordenadas das caixas
    confidences = results[0].boxes.conf  # Confiança de cada detecção
    classes = results[0].boxes.cls  # Classes das detecções
    labels = results[0].names  # Mapeia os índices de classe para nomes
  
    detections = []
    for i, box in enumerate(boxes):  
        detection = {
            "nome": labels[int(classes[i])], 
            "indice": int(classes[i]), 
            "confianca": float(confidences[i]),  # Confiança
            "caixa": {
                "x1": float(box[0]),  
                "y1": float(box[1]),  
                "x2": float(box[2]),  
                "y2": float(box[3])  
            }
        }
        detections.append(detection)
    
    return jsonify(detections)

def response_with_message(message, status_code=200):
    return jsonify({
        "message": message,
        "status_code": status_code
    }), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
