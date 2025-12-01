#!/bin/bash

echo "==================================="
echo "⚽ FBref Assists Analysis"
echo "Instalador Automático"
echo "==================================="
echo ""

# Detectar sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="Mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
else
    OS="Desconhecido"
fi

echo "📍 Sistema: $OS"
echo ""

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON="python3"
    PIP="pip3"
elif command -v python &> /dev/null; then
    PYTHON="python"
    PIP="pip"
else
    echo "❌ Python não encontrado!"
    echo "Instale Python 3.8+ de: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON --version 2>&1 | awk '{print $2}')
echo "✅ Python encontrado: $PYTHON_VERSION"
echo ""

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
$PYTHON -m venv venv

# Ativar ambiente virtual
if [[ "$OS" == "Windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Ambiente virtual ativado"
echo ""

# Instalar dependências
echo "📥 Instalando dependências..."
$PIP install --upgrade pip
$PIP install -r requirements.txt

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "==================================="
echo "Para executar o dashboard:"
echo ""
if [[ "$OS" == "Windows" ]]; then
    echo "  1. Execute: run.bat"
else
    echo "  1. Execute: ./run.sh"
fi
echo "  2. Aguarde carregar (primeira vez demora ~5 minutos)"
echo "  3. Abra o navegador em: http://localhost:8501"
echo "==================================="
