@echo off
REM Script para atualizar os dados do FBref

echo 🔄 Atualizando dados do FBref...

REM Verificar se existe ambiente virtual
if not exist "venv\" (
    echo ❌ Ambiente virtual não encontrado!
    echo Execute: python -m venv venv e depois install.bat
    exit /b 1
)

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Executar script de geração de dados
python generate_data.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Dados atualizados com sucesso!
    echo.
    echo 🐳 Para atualizar o Docker, execute:
    echo    docker-compose down
    echo    docker-compose build
    echo    docker-compose up -d
) else (
    echo ❌ Erro ao atualizar dados!
    exit /b 1
)

pause
