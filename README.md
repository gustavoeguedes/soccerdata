---
title: FBref Assists Analysis
emoji: ⚽
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.39.0"
app_file: streamlit_app.py
pinned: false
---

# ⚽ FBref Assists Analysis Dashboard

Análise de Assists vs Expected Assists (xAG) - Big 5 European Leagues (2017-2025)

## 📊 Funcionalidades

- **TOP 100 Overperformers**: Jogadores que geraram mais assists do que esperado
- **TOP 100 Subperformers**: Jogadores que geraram menos assists do que esperado  
- **TOP 100 Per 90 Minutes**: Performance normalizada por 90 minutos
- **Gráficos Interativos**: Visualizações com Plotly
- **Filtros Dinâmicos**: Liga, equipa, jogador, jogos mínimos, xAG mínimo

## 🚀 Tecnologias

- Python 3.11
- Streamlit
- soccerdata (FBref scraping)
- Pandas
- Plotly
- Matplotlib

## 📁 Estrutura

```
.
├── streamlit_app.py      # Dashboard principal
├── app.py                # Script CLI para exportar dados
├── requirements.txt      # Dependências Python
├── packages.txt          # Pacotes sistema (vazio)
├── .python-version       # Python 3.11
└── README.md             # Esta documentação
```

## 🔧 Executar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar dashboard
streamlit run streamlit_app.py

# Ou executar análise CLI
python app.py
```

## 🐳 Docker

### WSL Ubuntu (Recomendado)

```bash
# Build da imagem
./docker-build.sh

# Executar container
./docker-run.sh

# Acessar: http://localhost:8501

# Parar container
./docker-stop.sh
```

**Veja [DOCKER_WSL.md](DOCKER_WSL.md) para guia completo de instalação e configuração no WSL Ubuntu.**

### Docker Manual

```bash
# Build
docker build -t soccerdata-app .

# Run
docker run -d --name soccerdata-dashboard -p 8501:8501 soccerdata-app

# Stop
docker stop soccerdata-dashboard
```

### Docker Compose

```bash
# Build e executar
docker-compose up -d

# Parar
docker-compose down
```

## 📊 Dados

### Sistema Híbrido: CSV + FBref Live

O dashboard usa um **sistema inteligente de carregamento**:

1. **Prioridade 1 - CSV Local** (Rápido): Se existir `fbref_data.csv`, carrega instantaneamente
2. **Prioridade 2 - FBref Online** (Lento): Se CSV não existir, faz scraping do FBref

### Atualizar Dados

Para obter dados frescos do FBref:

**Linux/Mac:**
```bash
./update_data.sh
```

**Windows:**
```cmd
update_data.bat
```

O script irá:
- ✅ Fazer scraping do FBref
- ✅ Gerar novo `fbref_data.csv`
- ✅ Indicar como atualizar o Docker

### Por que CSV?

- **Docker/Cloud**: FBref bloqueia requisições de containers/cloud → CSV resolve
- **Performance**: Carregar CSV (1s) vs scraping FBref (5-10min)
- **Confiabilidade**: Não depende de conexão/disponibilidade do FBref

**Ligas incluídas:**
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (Inglaterra)
- 🇪🇸 La Liga (Espanha)
- 🇮🇹 Serie A (Itália)
- 🇩🇪 Bundesliga (Alemanha)
- 🇫🇷 Ligue 1 (França)

**Temporadas:** 2017-18 até 2024-25

## ⚠️ Nota

- **Primeira execução**: Se CSV não existir, scraping do FBref pode demorar 5-10 minutos
- **Docker**: Sempre use CSV (FBref bloqueia containers)
- **Atualização**: Execute `update_data.sh`/`.bat` mensalmente para dados frescos
