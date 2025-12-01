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

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip

echo.

REM Instalar dependencias (com fallback para wheels)
echo Instalando dependencias...
echo Tentando instalar pacotes pre-compilados...

REM Tentar instalar com wheels primeiro
pip install --only-binary :all: --upgrade wheel setuptools 2>nul
pip install soccerdata pandas matplotlib openpyxl plotly streamlit

if %errorlevel% neq 0 (
    echo.
    echo Instalacao normal falhou, tentando metodo alternativo...
    pip install --no-cache-dir soccerdata pandas matplotlib openpyxl plotly streamlit
)

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
