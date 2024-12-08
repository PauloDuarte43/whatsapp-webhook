# Usando a imagem oficial do Python como base
FROM python:3.10-slim

# Instalar pacotes de compilação necessários
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpcre3-dev \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de requisitos para o container
COPY requirements.txt /app/

# Instalar as dependências, incluindo uWSGI
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uwsgi  # Instalando o uWSGI

# Copiar o código fonte para o diretório de trabalho
COPY . /app/

# Definir o comando para iniciar a aplicação com uWSGI
CMD ["uwsgi", "--http", "0.0.0.0:5000", "-w", "app:app", "--master", "--processes", "10", "--threads", "2"]
