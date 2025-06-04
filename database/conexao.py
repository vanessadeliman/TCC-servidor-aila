import mysql.connector
from mysql.connector import Error
import os
from verificacoes import *
from modelos.usuario import *

# Variáveis de ambiente para MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

# Função para conectar ao MySQL
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        if connection.is_connected():
            print(f"Conexão bem-sucedida ao banco de dados MySQL '{MYSQL_DB}'")
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None