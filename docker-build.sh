#!/bin/bash

# Script para build da imagem Docker no WSL Ubuntu
# Autor: GitHub Copilot
# Data: 2025-12-01

set -e  # Exit on error

echo "================================================"
echo "  🐳 Build Docker - FBref Assists Analysis"
echo "================================================"
echo ""

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Erro: Docker não está instalado!"
    echo ""
    echo "Para instalar Docker no WSL Ubuntu, execute:"
    echo "  sudo apt update"
    echo "  sudo apt install docker.io -y"
    echo "  sudo usermod -aG docker \$USER"
    echo "  newgrp docker"
    exit 1
fi

# Verificar se Docker está rodando
if ! sudo docker info &> /dev/null; then
    echo "⚠️  Docker não está rodando. Tentando iniciar..."
    sudo service docker start
    sleep 2
fi

echo "🔨 Construindo imagem Docker..."
echo ""

# Build com docker-compose
if command -v docker-compose &> /dev/null; then
    sudo docker-compose build
else
    # Build com docker
    sudo docker build -t soccerdata-dashboard .
fi

echo ""
echo "✅ Build concluído com sucesso!"
echo ""
echo "Para executar o container, use:"
echo "  ./docker-run.sh"
echo ""
