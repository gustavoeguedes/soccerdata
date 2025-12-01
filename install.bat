@echo off
echo ===================================
echo Instalador FBref Assists Analysis
echo ===================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python nao encontrado!
    echo Instale de: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

echo Ambiente virtual ativado
echo.

REM Instalar dependencias
echo Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ===================================
echo Instalacao concluida!
echo.
echo Para executar:
echo   1. Clique em run.bat
echo   2. Aguarde carregar
echo   3. Abra: http://localhost:8501
echo ===================================
pause
