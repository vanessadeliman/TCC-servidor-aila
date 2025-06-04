# modelo_treinado/modelo_treinado.py
import os
import requests
from ultralytics import YOLO

MODEL_URL = os.getenv("MODEL_URL")
MODEL_PATH = os.getenv("MODEL_PATH")

model = None

def download_model():
    global model 
    if not os.path.exists(MODEL_PATH):
        print("Baixando o modelo...")
        response = requests.get(MODEL_URL, stream=True)
        if response.status_code == 200:
            with open(MODEL_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Modelo baixado com sucesso!")
        else:
            print(f"Falha ao baixar o modelo. Código de status: {response.status_code}")

    try:
        model = YOLO(MODEL_PATH)
        print("Modelo YOLO carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar o modelo YOLO: {e}")
        raise

def get_model():
    if model is None:
        print("Aviso: Tentando acessar o modelo YOLO antes de ser carregado. Chamando download_model()...")
        download_model()
    return model