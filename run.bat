@echo off
echo Iniciando FBref Assists Analysis...
echo.

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Executar Streamlit
echo Abrindo dashboard...
echo URL: http://localhost:8501
echo.
echo Pressione Ctrl+C para parar
echo.

streamlit run streamlit_app.py
