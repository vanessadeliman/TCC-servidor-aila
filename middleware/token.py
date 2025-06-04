# middleware/token.py
from flask import request, jsonify
from functools import wraps
from verificacoes import validar_jwt

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
            return jsonify({"message": f"Token inválido ou expirado: {str(e)}"}), 401

        return func(*args, **kwargs)
    return wrapper