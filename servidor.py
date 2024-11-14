from flask import Flask, request, jsonify
from ultralytics import YOLO
import io
from PIL import Image

app = Flask(__name__)
model = YOLO("/Users/eres/Downloads/imagens-semen/runs/detect/train/weights/best.pt")

@app.route('/analyze', methods=['POST'])
def analyze():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
