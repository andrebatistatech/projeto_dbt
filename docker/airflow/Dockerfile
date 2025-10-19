FROM apache/airflow:2.8.1-python3.11

# Mudar para root para instalar dependências do sistema
USER root

# Instalar dependências do sistema necessárias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Voltar para o usuário airflow
USER airflow

# Copiar requirements para instalar dependências Python
COPY requirements.txt /requirements.txt

# Instalar dependências Python
RUN pip install --no-cache-dir -r /requirements.txt

# Definir diretório de trabalho
WORKDIR /opt/airflow