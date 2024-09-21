# Use uma imagem base do Python
FROM python:3.10-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requirements
COPY requirements.txt /app/

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . /app/

# Defina as variáveis de ambiente
ENV DJANGO_SETTINGS_MODULE=precodebanana.settings
ENV PYTHONUNBUFFERED=1

# Execute a coleta de arquivos estáticos
RUN python manage.py collectstatic --noinput

# Exponha a porta em que o Django será executado
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "precodebanana.wsgi:application"]
