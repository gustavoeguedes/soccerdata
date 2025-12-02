#!/bin/bash

# Script para executar o container Docker no WSL Ubuntu
# Autor: GitHub Copilot
# Data: 2025-12-01

set -e  # Exit on error

echo "================================================"
echo "  🐳 Run Docker - FBref Assists Analysis"
echo "================================================"
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Erro: Docker não está instalado!"
    exit 1
fi

# Verificar se Docker está rodando
if ! sudo docker info &> /dev/null; then
    echo "⚠️  Docker não está rodando. Tentando iniciar..."
    sudo service docker start
    sleep 2
fi

# Parar container anterior se existir
if [ "$(sudo docker ps -aq -f name=soccerdata-dashboard)" ]; then
    echo "🛑 Parando container anterior..."
    sudo docker stop soccerdata-dashboard 2>/dev/null || true
    sudo docker rm soccerdata-dashboard 2>/dev/null || true
fi

echo "🚀 Iniciando container..."
echo ""

# Executar com docker-compose
if command -v docker-compose &> /dev/null; then
    sudo docker-compose up -d
else
    # Executar com docker
    sudo docker run -d \
        --name soccerdata-dashboard \
        -p 8501:8501 \
        -v $(pwd)/cache:/app/cache \
        -v $(pwd)/streamlit_app.py:/app/streamlit_app.py \
        -v $(pwd)/app.py:/app/app.py \
        --restart unless-stopped \
        soccerdata-dashboard
fi

echo ""
echo "✅ Container iniciado com sucesso!"
echo ""
echo "📊 Dashboard disponível em:"
echo "   http://localhost:8501"
echo ""
echo "Para ver os logs, execute:"
echo "   sudo docker logs -f soccerdata-dashboard"
echo ""
echo "Para parar o container, execute:"
echo "   sudo docker stop soccerdata-dashboard"
echo ""
