# routes/cadastro.py

from binascii import Error
from flask import jsonify, request

from database.conexao import create_db_connection
from modelos.usuario import Usuario
from verificacoes import criar_jwt, gerar_hash

def cadastro():
    connection = create_db_connection()
    if not connection:
        return jsonify({"message": "Erro de conexão com o banco de dados"}), 500

    cursor = None # Inicializa cursor

    try:

        body = request.get_json()
        
        if not body:
            return jsonify({"message": "Corpo da requisição vazio."}), 400
        if 'email' not in body:
             return jsonify({"message": "Email ausente no corpo da requisição."}), 400

        usuario = Usuario.from_json(body)

        cursor = connection.cursor(dictionary=True)

        query_select = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(query_select, (usuario.email,))
        usuario_existente = cursor.fetchone()

        senha_hash = gerar_hash(usuario.senha)

        if usuario_existente:
            query_update = """
            UPDATE usuarios
            SET nome = %s, instituicao = %s, senha = %s
            WHERE email = %s
            """
            cursor.execute(query_update, (usuario.nome, usuario.instituicao, senha_hash, usuario.email))
            connection.commit()
            print(f"Usuário atualizado: {usuario.email}")
        else:
            query_insert = """
            INSERT INTO usuarios (nome, email, instituicao, senha)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_insert, (usuario.nome, usuario.email, usuario.instituicao, senha_hash))
            connection.commit()
            print(f"Usuário inserido: {usuario.email}")

        usuario_json = usuario.tojson()
        jwt = criar_jwt(usuario_json)
        return jsonify({"AcessToken": jwt})

    except Error as e:
        connection.rollback()
        print(f"Erro no cadastro: {e}")
        return jsonify({"message": f"Erro interno do servidor: {e}"}), 500 # <--- RETURN EM CASO DE ERRO MYSQL
    except Exception as e:
        print(f"Erro inesperado no cadastro: {e}")
        return jsonify({"message": f"Erro inesperado: {e}"}), 500 # <--- RETURN EM CASO DE ERRO INESPERADO
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("Conexão MySQL fechada.")