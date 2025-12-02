@echo off
echo ===================================
echo FBref Assists Analysis Dashboard
echo ===================================
echo.

REM Verificar se venv existe
if not exist "venv\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado!
    echo.
    echo Execute primeiro: install.bat
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo ERRO: Falha ao ativar ambiente virtual
    pause
    exit /b 1
)

echo.
echo ===================================
echo Abrindo dashboard...
echo ===================================
echo.
echo URL: http://localhost:8501
echo.
echo Aguarde carregar dados (5-10 min primeira vez)
echo.
echo Pressione Ctrl+C para parar
echo.

REM Executar Streamlit
python -m streamlit run streamlit_app.py

if %errorlevel% neq 0 (
    echo.
    echo ===================================
    echo ERRO ao executar Streamlit
    echo ===================================
    echo.
    echo Possiveis causas:
    echo 1. Streamlit nao instalado - Execute install.bat
    echo 2. Porta 8501 ocupada - Feche outros processos
    echo.
    pause
    exit /b 1
)

pause
