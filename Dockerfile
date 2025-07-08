FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY servidor.py servidor.py
COPY modelo_treinado/modelo-treinado.pt modelo_treinado/modelo-treinado.pt

COPY modelo_treinado/ modelo_treinado/
COPY routes/ routes/

EXPOSE 5000

CMD ["python", "servidor.py"]
