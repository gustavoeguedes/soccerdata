#!/bin/bash

# Script para atualizar os dados do FBref

echo "🔄 Atualizando dados do FBref..."

# Ativar ambiente virtual
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Executar script de geração de dados
python generate_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Dados atualizados com sucesso!"
    echo ""
    echo "🐳 Para atualizar o Docker, execute:"
    echo "   ./docker-stop.sh"
    echo "   ./docker-build.sh"
    echo "   ./docker-run.sh"
else
    echo "❌ Erro ao atualizar dados!"
    exit 1
fi
