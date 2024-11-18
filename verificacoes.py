import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv
import base64

def decode_basic_auth(auth_header):
    if auth_header.startswith("Basic "):
        encoded_credentials = auth_header[6:]
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode('utf-8')
        usuario, senha = decoded_str.split(":", 1)
        return usuario, senha
    else:
        raise ValueError("Cabeçalho de autorização inválido")
    
def gerar_hash(senha):
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt)
    return senha_hash

def verificar_senha(senha, senha_hash):
    senha_bytes = senha.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, senha_hash)

def criar_jwt(dados, expiracao_horas=24):
    try:
        expiracao = datetime.datetime.utcnow() + datetime.timedelta(hours=expiracao_horas)
        
        payload = {
            "dados": dados,
            "exp": expiracao 
        }
        
        load_dotenv()
        secret_key = os.getenv('SECRET_KEY')
        print(f"SECRET_KEY: {secret_key}") 

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
    except Exception as e:
        print(f"Erro ao criar JWT: {str(e)}")
        raise

def validar_jwt(token):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token expirado!"
    except jwt.InvalidTokenError:
        return None, "Token inválido!"