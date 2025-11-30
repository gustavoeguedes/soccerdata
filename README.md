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

```bash
docker build -t soccerdata-app .
docker run --rm -p 8501:8501 -v $(pwd):/app soccerdata-app streamlit run streamlit_app.py --server.address=0.0.0.0
```

## 📊 Dados

Dados obtidos via web scraping do **FBref.com** usando a biblioteca `soccerdata`.

**Ligas incluídas:**
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (Inglaterra)
- 🇪🇸 La Liga (Espanha)
- 🇮🇹 Serie A (Itália)
- 🇩🇪 Bundesliga (Alemanha)
- 🇫🇷 Ligue 1 (França)

**Temporadas:** 2017-18 até 2024-25

## ⚠️ Nota

O carregamento inicial pode demorar alguns minutos devido ao scraping do FBref. Os dados são cacheados após o primeiro carregamento.
