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
python -m pip install --upgrade pip wheel setuptools

echo.

REM Instalar dependencias APENAS com wheels pre-compiladas
echo Instalando dependencias (usando pacotes pre-compilados)...
echo.

REM Forcar uso de wheels - NUNCA compilar do codigo fonte
pip install --prefer-binary --only-binary=lxml,pyarrow,pandas,numpy soccerdata pandas matplotlib openpyxl plotly streamlit

if %errorlevel% neq 0 (
    echo.
    echo ===================================
    echo AVISO: Instalacao com wheels falhou
    echo Tentando sem lxml e pyarrow...
    echo ===================================
    echo.
    
    REM Instalar sem lxml/pyarrow (soccerdata vai instalar depois)
    pip install pandas matplotlib openpyxl plotly streamlit
    pip install soccerdata --no-deps
    pip install beautifulsoup4 html5lib requests PySocks Unidecode cloudscraper rich undetected-chromedriver
)

echo.
echo ===================================
echo Instalacao concluida!
echo.
echo Para executar:
echo   1. Clique em run.bat
echo   2. Aguarde carregar (5-10 min primeira vez)
echo   3. Abra: http://localhost:8501
echo ===================================
echo.
echo NOTA: Se aparecer erro de lxml,
echo instale Visual C++ Build Tools:
echo https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo.
pause
