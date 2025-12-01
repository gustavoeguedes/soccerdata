# 🐍 Como Instalar Python no Windows

## 📥 Download

1. **Acesse**: https://www.python.org/downloads/
2. **Clique** no botão amarelo **"Download Python 3.x.x"**
3. **Aguarde** o download do instalador (exe)

---

## ⚙️ Instalação (IMPORTANTE)

### **Passo 1: Executar Instalador**

1. **Clique duplo** no arquivo baixado (`python-3.x.x-amd64.exe`)
2. **⚠️ ATENÇÃO**: Na primeira tela:
   - ✅ **Marque** a caixa **"Add Python to PATH"** (MUITO IMPORTANTE!)
   - ✅ **Marque** a caixa **"Install launcher for all users"**

```
┌─────────────────────────────────────────┐
│  ☑ Install launcher for all users      │
│  ☑ Add Python 3.x to PATH    ← MARCAR! │
│                                         │
│  [Install Now]  [Customize Install]    │
└─────────────────────────────────────────┘
```

3. **Clique** em **"Install Now"** (instalação padrão)

### **Passo 2: Aguardar Instalação**

- Aguarde a barra de progresso completar
- Pode aparecer janela UAC (controle de conta) → Clique **"Sim"**

### **Passo 3: Finalizar**

- Quando aparecer **"Setup was successful"**
- Clique em **"Close"**

---

## ✅ Verificar Instalação

### **Método 1: Prompt de Comando**

1. Pressione `Win + R`
2. Digite: `cmd`
3. Pressione `Enter`
4. Digite:
   ```cmd
   python --version
   ```
5. Deve aparecer algo como: `Python 3.12.3`

### **Método 2: PowerShell**

1. Pressione `Win + X`
2. Escolha **"Windows PowerShell"** ou **"Terminal"**
3. Digite:
   ```powershell
   python --version
   pip --version
   ```

**Resultado esperado:**
```
Python 3.12.3
pip 24.0 from C:\Users\SeuNome\AppData\Local\Programs\Python\Python312\lib\site-packages\pip (python 3.12)
```

---

## ⚠️ Problemas Comuns

### **Erro: "python não é reconhecido como comando"**

**Causa**: Python não foi adicionado ao PATH

**Solução 1 - Reinstalar:**
1. Desinstalar Python (Painel de Controle → Programas)
2. Baixar novamente
3. **Marcar "Add Python to PATH"** antes de instalar

**Solução 2 - Adicionar PATH Manualmente:**
1. Abrir **Painel de Controle**
2. **Sistema** → **Configurações avançadas do sistema**
3. **Variáveis de Ambiente**
4. Em **"Variáveis do sistema"**, selecionar **"Path"** → **Editar**
5. **Novo** → Adicionar:
   ```
   C:\Users\SeuNome\AppData\Local\Programs\Python\Python312
   C:\Users\SeuNome\AppData\Local\Programs\Python\Python312\Scripts
   ```
6. **OK** em todas as janelas
7. **Reiniciar** o Prompt de Comando

### **Erro: "Microsoft Store abre ao digitar python"**

**Causa**: Alias do Windows 11/10

**Solução:**
1. Abrir **Configurações** (`Win + I`)
2. **Aplicativos** → **Recursos opcionais** → **Mais recursos do Windows**
3. **Executar aplicativo** (ou **App execution aliases**)
4. **Desativar** os aliases:
   - `python.exe` → OFF
   - `python3.exe` → OFF
5. Fechar e abrir novo terminal

### **Erro: pip não funciona**

**Solução:**
```cmd
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### **Erro: "Failed building wheel for lxml/pyarrow"**

**Causa**: Falta Visual Studio C++ Build Tools

**Solução - Instalar Build Tools:**
1. **Baixar**: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. **Executar** instalador
3. **Selecionar**: "Desenvolvimento para desktop com C++"
4. **Instalar** (demora ~6GB)

**Solução Alternativa - Usar wheels pré-compiladas:**
```cmd
# Atualizar pip primeiro
python -m pip install --upgrade pip

# Instalar dependências separadamente
pip install --only-binary :all: lxml pyarrow

# Depois instalar o resto
pip install -r requirements.txt
```

**Solução Rápida - Remover pyarrow:**
Se não funcionar, edite `requirements.txt` e remova:
- `lxml>=4.9.0`
- `pyarrow`

O soccerdata vai instalar essas dependências automaticamente.

---

## 🎯 Versão Recomendada

- **Python 3.12.x** (mais recente estável)
- **Python 3.11.x** (alternativa estável)
- **Python 3.10.x** (mínimo recomendado)

⚠️ **Evitar**: Python 3.13+ (muito recente, pode ter incompatibilidades)

---

## 🚀 Após Instalar Python

### **1. Atualizar pip:**
```cmd
python -m pip install --upgrade pip
```

### **2. Instalar o projeto:**

**Opção A - Fácil (Clique duplo):**
1. Clique duplo em `install.bat`
2. Aguarde instalação
3. Clique duplo em `run.bat`

**Opção B - Manual:**
```cmd
cd C:\caminho\para\soccerdata
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 📝 Comandos Úteis

```cmd
# Verificar Python
python --version

# Verificar pip
pip --version

# Listar pacotes instalados
pip list

# Instalar pacote
pip install nome-do-pacote

# Desinstalar pacote
pip uninstall nome-do-pacote

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Desativar ambiente virtual
deactivate
```

---

## 🔧 Ferramentas Adicionais (Opcional)

### **Visual Studio Code (Editor)**
- Download: https://code.visualstudio.com/
- Instalar extensão **Python** (Microsoft)

### **Git for Windows** (Controle de versão)
- Download: https://git-scm.com/download/win
- Útil para clonar projetos do GitHub

---

## 📞 Links Úteis

- **Python.org**: https://www.python.org/
- **Documentação**: https://docs.python.org/3/
- **pip**: https://pip.pypa.io/
- **Tutoriais**: https://www.python.org/about/gettingstarted/

---

## ✅ Checklist Final

Antes de executar o projeto, certifique-se:

- [ ] Python instalado (verificar com `python --version`)
- [ ] pip funcionando (verificar com `pip --version`)
- [ ] PATH configurado corretamente
- [ ] Prompt de Comando/PowerShell reconhece `python`
- [ ] Consegue criar ambiente virtual (`python -m venv teste`)

**Se todos os itens estão OK, está pronto para usar!** 🎉

---

**Criado para: FBref Assists Analysis**
**Versão: 1.0**
**Data: Novembro 2025**
