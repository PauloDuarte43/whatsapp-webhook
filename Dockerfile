# Usando a imagem oficial do Python como base
FROM python:3.10-slim

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
CMD ["uwsgi", "--http", "0.0.0.0:5000", "--wsgi-file", "app.py", "--master", "--processes", "10", "--threads", "2"]
