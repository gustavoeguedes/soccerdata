#!/bin/bash

echo "⚽ Iniciando FBref Assists Analysis..."
echo ""

# Ativar ambiente virtual
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Executar Streamlit
echo "🚀 Abrindo dashboard..."
echo "📍 URL: http://localhost:8501"
echo ""
echo "⏹️  Pressione Ctrl+C para parar"
echo ""

streamlit run streamlit_app.py
