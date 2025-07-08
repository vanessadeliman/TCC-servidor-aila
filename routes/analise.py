# routes/analise.py
from flask import request, jsonify
import io
from PIL import Image
from modelo_treinado.modelo_treinado import get_model

def analise():
    try:
        model = get_model() 

        img_file = request.files.get('image') 
        if not img_file:
            return jsonify({"message": "Nenhuma imagem fornecida"}), 400

        img_bytes = img_file.read()

        img = Image.open(io.BytesIO(img_bytes))

        results = model(img)

        boxes = results[0].boxes.xyxy
        confidences = results[0].boxes.conf
        classes = results[0].boxes.cls
        labels = results[0].names

        detections = []
        for i, box in enumerate(boxes):
            detection = {
                "nome": labels[int(classes[i])],
                "indice": int(classes[i]),
                "confianca": float(confidences[i]),
                "caixa": {
                    "x1": float(box[0]),
                    "y1": float(box[1]),
                    "x2": float(box[2]),
                    "y2": float(box[3])
                }
            }
            detections.append(detection)

        return jsonify(detections)
    except Exception as e:
        print(f"Erro durante o processamento da imagem: {str(e)}")
        return jsonify({"message": "Erro no servidor", "error": str(e)}), 500