# ⚽ FBref Assists Analysis - Python Project

Projeto completo em Python para análise de dados do FBref usando o pacote **soccerdata**. Analisa assistências vs expected assists (xAG) dos jogadores das Big 5 Leagues europeias entre 2017-2025.

---

## 📋 **PRÉ-REQUISITOS**

Antes de começar, certifique-se que tem instalado:

### **Opção 1: Docker (Recomendado)** ✅
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e a correr
  - **Windows**: Docker Desktop for Windows
  - **macOS**: Docker Desktop for Mac
  - **Linux**: Docker Engine

**Verificar instalação:**
```bash
docker --version
# Deve mostrar algo como: Docker version 24.x.x
```

### **Opção 2: Python Local** (alternativa)
- Python 3.10 ou superior
- pip (gestor de pacotes Python)

---

## 🚀 **INSTALAÇÃO E EXECUÇÃO**

### **📦 PASSO 1: Obter o Projeto**

**Opção A: Clonar repositório**
```bash
git clone <url-do-repositorio>
cd soccerdata
```

**Opção B: Download ZIP**
1. Descarregar o projeto como ZIP
2. Extrair para uma pasta (ex: `C:\Projects\soccerdata` ou `~/Projects/soccerdata`)
3. Abrir terminal/cmd na pasta extraída

---

### **🐳 MÉTODO 1: Usar Docker (Recomendado)**

#### **1.1. Build da Imagem Docker**

Abrir terminal na pasta do projeto e executar:

```bash
docker build -t soccerdata-app .
```

⏱️ **Tempo estimado**: 3-5 minutos (primeira vez)

**O que faz:** Cria uma imagem Docker com todas as dependências instaladas.

---

#### **1.2. Executar Análise (Gerar CSV/Excel/Gráficos)**

**Windows (PowerShell):**
```powershell
docker run --rm `
  -v ${PWD}:/app `
  -v ${PWD}/out:/app/out `
  -v ${PWD}/cache:/root/soccerdata/data `
  soccerdata-app
```

**Windows (CMD):**
```cmd
docker run --rm ^
  -v %cd%:/app ^
  -v %cd%/out:/app/out ^
  -v %cd%/cache:/root/soccerdata/data ^
  soccerdata-app
```

**macOS / Linux:**
```bash
docker run --rm \
  -v $(pwd):/app \
  -v $(pwd)/out:/app/out \
  -v $(pwd)/cache:/root/soccerdata/data \
  soccerdata-app
```

⏱️ **Tempo estimado**: 
- Primeira execução: 5-10 minutos (download de dados)
- Execuções seguintes: ~30 segundos (usa cache)

**Resultados:** Ficheiros gerados na pasta `out/`:
- `top100_subperformers.csv`
- `top100_overperformers.csv`
- `top100_per90.csv`
- `top100_assists_analysis.xlsx`
- `scatter_xag_vs_assists.png`
- `bar_top20_overperformers.png`
- `bar_top20_subperformers.png`

---

#### **1.3. Executar Dashboard Interativo (Streamlit)**

**Windows (PowerShell):**
```powershell
docker run --rm `
  -p 8501:8501 `
  -v ${PWD}:/app `
  -v ${PWD}/cache:/root/soccerdata/data `
  soccerdata-app `
  streamlit run streamlit_app.py --server.address=0.0.0.0
```

**Windows (CMD):**
```cmd
docker run --rm ^
  -p 8501:8501 ^
  -v %cd%:/app ^
  -v %cd%/cache:/root/soccerdata/data ^
  soccerdata-app ^
  streamlit run streamlit_app.py --server.address=0.0.0.0
```

**macOS / Linux:**
```bash
docker run --rm \
  -p 8501:8501 \
  -v $(pwd):/app \
  -v $(pwd)/cache:/root/soccerdata/data \
  soccerdata-app \
  streamlit run streamlit_app.py --server.address=0.0.0.0
```

⏱️ **Tempo estimado**: 2-3 minutos para carregar

**Aceder ao Dashboard:**
1. Abrir navegador
2. Ir para: **http://localhost:8501**
3. Aguardar carregamento dos dados

**Para parar:** Pressionar `Ctrl+C` no terminal

---

### **🐍 MÉTODO 2: Usar Python Local (Sem Docker)**

#### **2.1. Criar Ambiente Virtual**

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

---

#### **2.2. Instalar Dependências**

```bash
pip install soccerdata pandas polars numpy pyarrow matplotlib openpyxl streamlit plotly
```

⏱️ **Tempo estimado**: 2-3 minutos

---

#### **2.3. Executar Análise**

```bash
python app.py
```

**Resultados:** Ficheiros gerados na pasta `out/`

---

#### **2.4. Executar Dashboard**

```bash
streamlit run streamlit_app.py
```

**Aceder:** http://localhost:8501

---

## 📁 **ESTRUTURA DO PROJETO**

```
soccerdata/
├── app.py                      # Script principal de análise
├── streamlit_app.py            # Dashboard interativo
├── dockerfile                  # Configuração Docker
├── README.md                   # Este ficheiro
├── .dockerignore              # Ficheiros ignorados no build
├── .gitignore                 # Ficheiros ignorados no git
├── out/                       # 📊 Outputs (CSV, XLSX, PNG)
│   ├── top100_subperformers.csv
│   ├── top100_overperformers.csv
│   ├── top100_per90.csv
│   ├── top100_assists_analysis.xlsx
│   └── *.png
└── cache/                     # 💾 Cache do soccerdata
    └── fbref/
```

---

## 🎯 **FUNCIONALIDADES**

### **📊 Análise (app.py)**
- ✅ Carrega dados FBref das Big 5 Leagues (2017-2025)
- ✅ Calcula métricas: `assists_minus_xag` e `assists_minus_xag_90`
- ✅ Gera TOP 100 (Overperformers, Subperformers, Per 90)
- ✅ Exporta para CSV, Excel e gráficos PNG
- ✅ Sistema robusto com fallback automático

### **🖥️ Dashboard (streamlit_app.py)**
- ✅ Interface interativa com filtros (liga, equipa, jogador)
- ✅ Tabs separados para cada ranking TOP 100
- ✅ **5 Gráficos interativos Plotly:**
  - Scatter plot xAG vs Assists (com hover)
  - Top 30 Overperformers (bar chart)
  - Top 30 Subperformers (bar chart)
  - Distribuição por Liga (boxplot)
  - Top 20 por 90 minutos
- ✅ Download de CSV direto do dashboard
- ✅ Métricas resumidas no topo

---

## 🔧 **RESOLUÇÃO DE PROBLEMAS**

### **Problema: Docker não reconhecido**
**Solução:**
1. Instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Reiniciar computador
3. Abrir Docker Desktop
4. Tentar novamente

---

### **Problema: Porta 8501 já em uso**
**Solução:**
```bash
# Usar porta diferente (ex: 8502)
docker run --rm -p 8502:8501 ... streamlit run streamlit_app.py --server.address=0.0.0.0

# Aceder: http://localhost:8502
```

---

### **Problema: Download muito lento**
**Solução:**
- É normal na primeira execução (download de ~5-10 minutos)
- Execuções seguintes usam cache e são rápidas (~30s)
- Garantir boa conexão à internet

---

### **Problema: Erro "No module named 'soccerdata'"**
**Solução (Docker):**
```bash
docker build --no-cache -t soccerdata-app .
```

**Solução (Python local):**
```bash
pip install --upgrade soccerdata
```

---

### **Problema: Permissões negadas (Linux/Mac)**
**Solução:**
```bash
sudo docker run ...
# ou
sudo chmod -R 755 out/ cache/
```

---

## 💡 **DICAS E TRUQUES**

### **Limpar Cache**
```bash
# Limpar cache de dados (força re-download)
rm -rf cache/

# Windows:
rmdir /s cache
```

### **Ver Logs Detalhados**
```bash
# Guardar output num ficheiro
docker run ... soccerdata-app | tee analysis.log
```

### **Executar em Background (Streamlit)**
```bash
# Linux/Mac
docker run -d -p 8501:8501 ... streamlit run streamlit_app.py --server.address=0.0.0.0

# Ver logs
docker logs <container-id>

# Parar
docker stop <container-id>
```

### **Acelerar com Cache Persistente**
Os volumes `-v $(pwd)/cache:/root/soccerdata/data` garantem que:
- Dados são guardados entre execuções
- Não precisa re-download
- **Economia de 5-10 minutos por execução**

---

## 📊 **MÉTRICAS CALCULADAS**

| Métrica | Descrição | Fórmula |
|---------|-----------|---------|
| **assists_minus_xag** | Diferença entre assists reais e esperados | `assists - xAG` |
| **assists_minus_xag_90** | Métrica normalizada por 90 minutos | `(assists - xAG) / minutes * 90` |
| **Overperformers** | Jogadores com assists acima do esperado | `assists_minus_xag > 0` |
| **Subperformers** | Jogadores com assists abaixo do esperado | `assists_minus_xag < 0` |

---

## 🎓 **TUTORIAL PASSO A PASSO (Iniciantes)**

### **Para quem nunca usou Docker:**

1. **Instalar Docker Desktop**
   - Windows: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe
   - Mac: https://desktop.docker.com/mac/main/amd64/Docker.dmg
   - Seguir instalação padrão

2. **Descarregar projeto**
   - Download ZIP do repositório
   - Extrair para `C:\Users\SeuNome\soccerdata`

3. **Abrir terminal na pasta**
   - Windows: Shift + Clique direito na pasta → "Abrir janela do PowerShell aqui"
   - Mac: Botão direito → "New Terminal at Folder"

4. **Build (só uma vez)**
   ```bash
   docker build -t soccerdata-app .
   ```
   Aguardar ~5 minutos

5. **Executar Dashboard**
   - Copiar comando do PASSO 1.3 (para seu sistema)
   - Colar no terminal
   - Pressionar Enter
   - Abrir http://localhost:8501

6. **Parar**
   - Pressionar `Ctrl+C` no terminal

**Pronto! 🎉**

---

## 📖 **DOCUMENTAÇÃO ADICIONAL**

### **Formato de Temporadas**
O soccerdata aceita múltiplos formatos:
- `'1718'` ✅ (recomendado)
- `'2017-18'` ✅
- `'2017-2018'` ✅
- `2017` ✅
- `[17, 18, 19]` ✅

### **Ligas Disponíveis**
```python
import soccerdata as sd
print(sd.FBref.available_leagues())
```

Output:
```
['Big 5 European Leagues Combined', 
 'ENG-Premier League', 
 'ESP-La Liga', 
 'FRA-Ligue 1', 
 'GER-Bundesliga', 
 'ITA-Serie A',
 'INT-World Cup',
 "INT-Women's World Cup"]
```

---

## 🤝 **CONTRIBUIR**

Melhorias sugeridas:
- [ ] Adicionar mais ligas
- [ ] Análise temporal (evolução por temporada)
- [ ] Comparação entre jogadores
- [ ] Exportar relatório PDF
- [ ] API REST

---

## 📄 **LICENÇA**

Projeto livre para uso pessoal e educacional.

**Dados:** FBref via pacote soccerdata

---

## 🆘 **SUPORTE**

**Problemas comuns já resolvidos acima ☝️**

**Ainda com dúvidas?**
1. Verificar se Docker está a correr
2. Verificar conexão à internet
3. Ler mensagens de erro completas
4. Consultar secção "Resolução de Problemas"

---

## 📞 **COMANDOS RÁPIDOS**

```bash
# Build
docker build -t soccerdata-app .

# Análise completa
docker run --rm -v $(pwd):/app -v $(pwd)/out:/app/out -v $(pwd)/cache:/root/soccerdata/data soccerdata-app

# Dashboard
docker run --rm -p 8501:8501 -v $(pwd):/app -v $(pwd)/cache:/root/soccerdata/data soccerdata-app streamlit run streamlit_app.py --server.address=0.0.0.0

# Limpar tudo
docker system prune -a
rm -rf cache/ out/
```

---

**Desenvolvido com ❤️ usando Python, Polars, Streamlit, Plotly e Docker**

⚽ Big 5 Leagues | 📊 2017-2025 | 🚀 Powered by FBref
