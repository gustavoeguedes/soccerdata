# ⚽ FBref Assists Analysis - Instalação Cliente

## 📋 Requisitos

- **Python 3.8+** instalado
- **Conexão com internet** (primeira execução)
- **5-10 minutos** para carregar dados (primeira vez)

---

## 🚀 Instalação Rápida

### **Windows**

1. **Baixar o projeto**:
   - Fazer download do ZIP ou clonar: `git clone https://github.com/gustavoeguedes/soccerdata.git`

2. **Instalar**:
   
   **Opção A - Instalação Normal (recomendado):**
   - Clique duplo em `install.bat`
   - Aguarde instalação das dependências
   
   **Opção B - SEM Visual Studio C++ (se a Opção A falhar):**
   - Clique duplo em `install_sem_build.bat`
   - Usa pacotes pré-compilados (pula lxml/pyarrow problemáticos)

3. **Executar**:
   - Clique duplo em `run.bat`
   - Aguarde abrir o navegador em `http://localhost:8501`

**⚠️ Se aparecer erro "Microsoft Visual C++ 14.0 required":**
- Use `install_sem_build.bat` OU
- Instale Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

### **Linux / Mac**

1. **Baixar o projeto**:
   ```bash
   git clone https://github.com/gustavoeguedes/soccerdata.git
   cd soccerdata
   ```

2. **Dar permissão e instalar**:
   ```bash
   chmod +x install.sh run.sh
   ./install.sh
   ```

3. **Executar**:
   ```bash
   ./run.sh
   ```

4. **Abrir navegador**: http://localhost:8501

---

## 📦 Instalação Manual

Se os scripts automáticos não funcionarem:

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar dashboard
streamlit run streamlit_app.py
```

---

## ⚙️ Configuração

### **Cache de Dados**

Os dados do FBref são salvos em `cache/` na primeira execução. Isso acelera carregamentos futuros.

Para limpar cache e recarregar dados:
- **Windows**: Deletar pasta `cache/`
- **Linux/Mac**: `rm -rf cache/`

### **Exportar Dados**

Para gerar arquivos CSV/Excel/PNG:

```bash
# Ativar ambiente primeiro
python app.py
```

Arquivos serão salvos em `out/`:
- `top100_overperformers.csv`
- `top100_subperformers.csv`
- `top100_per90.csv`
- `top100_assists_analysis.xlsx`
- 3 gráficos PNG

---

## 🐛 Troubleshooting

### **Erro: Python não encontrado**

**Solução**: Instalar Python de https://www.python.org/downloads/

### **Erro: Timeout ao carregar dados**

**Soluções**:
1. Verificar conexão com internet
2. Tentar novamente (FBref pode estar lento)
3. Usar menos temporadas (editar `streamlit_app.py` linha 88)

### **Erro: ModuleNotFoundError**

**Solução**:
```bash
pip install -r requirements.txt
```

### **Porta 8501 ocupada**

**Solução**: Alterar porta:
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 📊 Uso

### **Dashboard Interativo**

1. **Filtros** (barra lateral):
   - Liga
   - Equipa
   - Jogador (busca)
   - Jogos mínimos
   - xAG mínimo

2. **Tabs**:
   - 🔺 **Overperformers**: TOP 100 com mais assists que esperado
   - 🔻 **Subperformers**: TOP 100 com menos assists que esperado
   - ⚡ **Per 90**: TOP 100 normalizado por 90 minutos
   - 📈 **Gráficos**: Visualizações interativas (Plotly)

3. **Download CSV**: Botão em cada tab

---

## 🔄 Atualizar Dados

Dados são atualizados automaticamente a cada 1 hora (cache).

Para forçar atualização:
1. Limpar cache (deletar pasta `cache/`)
2. Recarregar página no dashboard (F5)

---

## 📁 Estrutura

```
soccerdata/
├── streamlit_app.py      # Dashboard principal
├── app.py                # Script CLI
├── requirements.txt      # Dependências
├── install.bat/.sh       # Instalador
├── run.bat/.sh           # Executar dashboard
├── cache/                # Cache FBref
└── out/                  # Exportações CSV/Excel/PNG
```

---

## 🎯 Funcionalidades

- ✅ **5 Ligas Europeias**: Premier League, La Liga, Serie A, Bundesliga, Ligue 1
- ✅ **8 Temporadas**: 2017-18 até 2024-25
- ✅ **TOP 100 Rankings**: Overperformers, Subperformers, Per 90
- ✅ **Filtros Dinâmicos**: Liga, equipa, jogador, estatísticas
- ✅ **Gráficos Interativos**: Scatter, Bar, Boxplot (Plotly)
- ✅ **Exportação**: CSV, Excel, PNG
- ✅ **Cache Inteligente**: Acelera recarregamentos

---

## 💡 Dicas

1. **Primeira execução**: Demora ~5-10 minutos (carregando dados FBref)
2. **Cache**: Próximas execuções são instantâneas
3. **Filtros**: Use para análises específicas
4. **Download**: Exporte rankings para Excel/Google Sheets

---

## 📞 Suporte

- **GitHub**: https://github.com/gustavoeguedes/soccerdata
- **Issues**: Reportar bugs/sugestões

---

## 📄 Licença

MIT License - Uso livre para análises pessoais e comerciais.

---

**Desenvolvido com Python + Streamlit + soccerdata + Plotly** 🚀
