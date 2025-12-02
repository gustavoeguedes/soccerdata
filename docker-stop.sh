#!/bin/bash

# Script para parar o container Docker no WSL Ubuntu
# Autor: GitHub Copilot
# Data: 2025-12-01

echo "================================================"
echo "  🛑 Stop Docker - FBref Assists Analysis"
echo "================================================"
echo ""

# Parar com docker-compose
if command -v docker-compose &> /dev/null && [ -f docker-compose.yml ]; then
    echo "🛑 Parando container via docker-compose..."
    sudo docker-compose down
else
    # Parar com docker
    if [ "$(sudo docker ps -q -f name=soccerdata-dashboard)" ]; then
        echo "🛑 Parando container..."
        sudo docker stop soccerdata-dashboard
        sudo docker rm soccerdata-dashboard
    else
        echo "ℹ️  Container não está rodando."
    fi
fi

echo ""
echo "✅ Container parado com sucesso!"
echo ""
