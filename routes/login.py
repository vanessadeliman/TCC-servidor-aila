# routes/login.py
from flask import request, jsonify
import mysql.connector
from mysql.connector import Error
import os

from verificacoes import criar_jwt, decode_basic_auth, verificar_senha

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def login():
    connection = create_db_connection()
    if not connection:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500

    try:
        auth_header = request.headers.get('Authorization')
        email, senha = decode_basic_auth(auth_header)

        cursor = connection.cursor(dictionary=True)
        query_select = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query_select, (email,))
        usuario = cursor.fetchone()

        if usuario:
            if verificar_senha(senha, usuario["senha"]):
                usuario_json = {
                    "nome": usuario.get("nome"),
                    "instituicao": usuario.get("instituicao")
                }
                jwt = criar_jwt(usuario_json)
                usuario_json["AcessToken"] = jwt
                return jsonify(usuario_json), 200
            else:
                return jsonify({"message": "Senha inválida"}), 401
        else:
            return jsonify({"message": "Usuário não encontrado"}), 404

    except Error as e:
        print(f"Erro no login: {e}")
        return jsonify({"message": f"Erro interno do servidor: {e}"}), 500
    except Exception as e:
        print(f"Erro inesperado no login: {e}")
        return jsonify({"message": f"Erro inesperado: {e}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()