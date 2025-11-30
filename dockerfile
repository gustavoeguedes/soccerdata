FROM python:3.10-bullseye

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    python3-distutils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python necessárias (SEM Selenium/Chrome)
RUN pip install --no-cache-dir \
    soccerdata \
    pandas \
    polars \
    numpy \
    pyarrow \
    matplotlib \
    openpyxl \
    streamlit \
    plotly

# Copiar o teu código para dentro da imagem
COPY . .

# Diretório para outputs
RUN mkdir -p /app/out

# Comando padrão
CMD ["python", "app.py"]
