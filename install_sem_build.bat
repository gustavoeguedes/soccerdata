@echo off
echo ===================================
echo Instalador ALTERNATIVO - Sem Build
echo Para Windows sem Visual Studio
echo ===================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Erro: Python nao encontrado!
    pause
    exit /b 1
)

echo Python encontrado!
echo.

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo.
echo Atualizando pip...
python -m pip install --upgrade pip wheel

echo.
echo Instalando pacotes basicos...
pip install pandas matplotlib openpyxl plotly streamlit

echo.
echo Instalando BeautifulSoup e dependencias...
pip install beautifulsoup4 html5lib requests

echo.
echo Instalando soccerdata (sem dependencias problematicas)...
pip install --no-deps soccerdata

echo.
echo Instalando dependencias restantes...
pip install PySocks Unidecode cloudscraper packaging rich websockets
pip install selenium trio trio-websocket websocket-client undetected-chromedriver

echo.
echo ===================================
echo Instalacao ALTERNATIVA concluida!
echo.
echo AVISO: lxml e pyarrow foram pulados
echo A maioria das funcoes deve funcionar
echo.
echo Para executar:
echo   1. Clique em run.bat
echo   2. Aguarde carregar
echo   3. Abra: http://localhost:8501
echo ===================================
pause
