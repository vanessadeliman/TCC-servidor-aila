FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos para o contêiner
COPY . /app

# Instalar dependências do Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Comando padrão
CMD ["python", "servidor.py"]
