FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY servidor.py servidor.py

COPY modelo_treinado/ modelo_treinado/
COPY routes/ routes/

EXPOSE 5000

CMD ["python", "servidor.py"]
