# 🎯 Guia Rápido de Uso

## ✅ Sistema Funcionando

O dashboard agora usa **sistema híbrido** que resolve o problema do FBref bloquear Docker/Cloud.

## 📊 Como Funciona

### 1️⃣ Carregamento Inteligente

```
┌─────────────────────────────┐
│  Dashboard Streamlit        │
└──────────┬──────────────────┘
           │
           ▼
    ┌──────────────┐
    │ fbref_data.csv │ ◄─── PRIORIDADE 1: CSV Local (1s)
    │   existe?     │
    └──────┬───────┘
           │
           │ NÃO
           ▼
    ┌──────────────┐
    │ FBref.com    │ ◄─── PRIORIDADE 2: Scraping Online (5-10min)
    │   scraping   │
    └──────────────┘
```

### 2️⃣ Situações

| Situação | O que acontece |
|----------|----------------|
| **Docker/Cloud** | ✅ Usa CSV (FBref bloqueia containers) |
| **Local sem CSV** | ⚠️ Faz scraping do FBref (demora) |
| **Local com CSV** | ✅ Carrega instantâneo do CSV |

## 🚀 Uso Básico

### Docker (Recomendado)

```bash
# 1. Build (apenas primeira vez ou após atualizar código)
./docker-build.sh

# 2. Executar
./docker-run.sh

# 3. Acessar
http://localhost:8501

# 4. Parar
./docker-stop.sh
```

### Local

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

## 🔄 Atualizar Dados

Para obter dados frescos do FBref (recomendado mensalmente):

### Linux/Mac

```bash
# Atualizar CSV
./update_data.sh

# Rebuild Docker (se usar)
./docker-stop.sh
./docker-build.sh
./docker-run.sh
```

### Windows

```cmd
# Atualizar CSV
update_data.bat

# Rebuild Docker (se usar)
docker-compose down
docker-compose build
docker-compose up -d
```

## ⚙️ Troubleshooting

### Docker não inicia

```bash
# Verificar se Docker está rodando
sudo systemctl status docker

# Iniciar Docker
sudo systemctl start docker

# Verificar logs
sudo docker logs soccerdata-dashboard
```

### CSV desatualizado

```bash
# Regenerar CSV
./update_data.sh  # Linux/Mac
update_data.bat   # Windows
```

### Erro "Could not download FBref"

✅ **Solução**: Isso é esperado no Docker. O sistema automaticamente usa o CSV.

Se ver este erro **localmente** (fora do Docker):

1. Verifique conexão com internet
2. Tente novamente (FBref pode estar temporariamente indisponível)
3. Use `./update_data.sh` para forçar novo scraping

## 📁 Arquivos Importantes

```
soccerdata/
├── fbref_data.csv           # Dados pré-carregados (648KB)
├── streamlit_app.py         # Dashboard principal
├── generate_data.py         # Script para gerar CSV
├── update_data.sh/.bat      # Atualizar dados
├── docker-build.sh          # Build Docker
├── docker-run.sh            # Executar Docker
└── docker-stop.sh           # Parar Docker
```

## 🎨 Funcionalidades do Dashboard

1. **TOP 100 Overperformers**: Jogadores que geraram mais assists que esperado
2. **TOP 100 Subperformers**: Jogadores abaixo da expectativa
3. **TOP 100 Per 90 Minutes**: Normalizado por tempo de jogo
4. **Gráficos Interativos Plotly**: Zoom, hover, filtros
5. **Filtros Dinâmicos**: Liga, equipa, jogador, mínimos

## 📊 Dados Incluídos

- **Ligas**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- **Temporadas**: 2017-18 até 2024-25
- **Jogadores**: ~7500 jogadores
- **Registros**: ~22000 linhas
- **Tamanho**: 648KB

## ⚡ Performance

| Método | Tempo de Carregamento |
|--------|----------------------|
| CSV Local | ~1 segundo |
| FBref Scraping | 5-10 minutos |

## 🔒 Limitações do FBref

O FBref.com bloqueia:
- ❌ Cloud IPs (Streamlit Cloud, Hugging Face)
- ❌ Docker containers
- ❌ Data centers
- ✅ IPs residenciais (seu PC local)

**Solução**: Usar CSV pré-carregado para Docker/Cloud.

## 💡 Dicas

1. **Docker**: Sempre use CSV (FBref bloqueia)
2. **Atualização**: CSV mensal é suficiente
3. **Performance**: CSV é 300x+ mais rápido que scraping
4. **Confiabilidade**: CSV não depende de FBref estar online
5. **Backup**: Mantenha `fbref_data.csv` versionado

## 📝 Próximos Passos

1. ✅ Sistema híbrido funcionando
2. ✅ Docker configurado
3. ✅ Scripts de atualização criados
4. 🔄 Agendar atualização mensal (cron/Task Scheduler)
5. 🔄 Deploy em servidor privado (se necessário)

## 🆘 Suporte

Veja documentação completa:
- `README.md` - Visão geral
- `DOCKER_WSL.md` - Docker no WSL Ubuntu
- `INSTALL.md` - Instalação local
- `PYTHON_WINDOWS.md` - Python no Windows
