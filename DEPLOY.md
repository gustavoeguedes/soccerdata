# ⚽ FBref Assists Analysis - Deploy Streamlit Cloud

## 📋 **GUIA DE DEPLOY NO STREAMLIT CLOUD**

### **✅ Pré-requisitos**
- Conta no GitHub (gratuita)
- Conta no Streamlit Cloud (gratuita): https://share.streamlit.io

---

## 🚀 **PASSO A PASSO COMPLETO**

### **1️⃣ Criar Repositório no GitHub**

1. Aceder a https://github.com
2. Clicar em **"New repository"** (botão verde)
3. Configurar:
   - **Repository name**: `soccerdata-fbref`
   - **Description**: `FBref Assists Analysis Dashboard`
   - **Public** ✅ (necessário para Streamlit Cloud gratuito)
   - **NÃO** marcar "Add a README" (já temos)
4. Clicar em **"Create repository"**

---

### **2️⃣ Fazer Push do Código para GitHub**

**Na pasta do projeto, executar:**

```bash
# Inicializar git (se ainda não foi feito)
git init

# Adicionar todos os ficheiros
git add .

# Fazer commit
git commit -m "Initial commit - FBref Assists Analysis"

# Adicionar remote (substituir SEU_USERNAME pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USERNAME/soccerdata-fbref.git

# Fazer push
git branch -M main
git push -u origin main
```

**Verificar:** Os ficheiros devem aparecer no GitHub

---

### **3️⃣ Deploy no Streamlit Cloud**

1. **Aceder a:** https://share.streamlit.io
2. **Login** com GitHub
3. Clicar em **"New app"**
4. Configurar:
   - **Repository**: `SEU_USERNAME/soccerdata-fbref`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **App URL** (opcional): escolher URL customizado
5. Clicar em **"Deploy!"**

⏱️ **Tempo estimado**: 5-10 minutos (primeira vez)

---

### **4️⃣ Aguardar Deploy**

O Streamlit Cloud vai:
1. ✅ Clonar repositório
2. ✅ Instalar dependências (`requirements.txt`)
3. ✅ Executar `streamlit_app.py`
4. ✅ Disponibilizar URL público

**Logs aparecerão em tempo real**

---

### **5️⃣ Aceder à Aplicação**

Quando deploy terminar:
- URL será algo como: `https://seu-username-soccerdata-fbref-streamlitapp-xyz.streamlit.app`
- Guardar URL para partilhar
- App está **público** e **disponível 24/7**

---

## 📁 **Ficheiros Necessários (já criados)**

### ✅ `requirements.txt`
Lista todas as dependências Python:
```
soccerdata
pandas
polars
numpy
pyarrow
matplotlib
openpyxl
streamlit
plotly
```

### ✅ `.streamlit/config.toml`
Configurações do Streamlit (tema, servidor):
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
enableCORS = false
port = 8501
```

### ✅ `packages.txt`
Pacotes do sistema (se necessário):
```
# Vazio por enquanto
```

### ✅ `.gitignore`
Já existe - ignora cache e outputs

---

## ⚙️ **Alterações Feitas no Código**

### **1. Cache com TTL**
```python
@st.cache_data(show_spinner=False, ttl=3600)  # Cache por 1 hora
```
- Evita recarregar dados a cada visita
- Cache expira após 1 hora
- Reduz consumo de recursos

### **2. Try-Catch no load_data()**
```python
try:
    fbref = sd.FBref(...)
except Exception as e:
    st.error(f"❌ Erro: {e}")
    return None
```
- Captura erros de conexão
- Mostra mensagens amigáveis
- Não quebra a aplicação

---

## 🔧 **Configurações Opcionais**

### **Secrets (Dados Sensíveis)**

Se precisar de API keys ou senhas:

1. No Streamlit Cloud, ir em **"Settings" → "Secrets"**
2. Adicionar no formato TOML:
```toml
[api]
key = "sua_chave_aqui"
```

3. Aceder no código:
```python
import streamlit as st
api_key = st.secrets["api"]["key"]
```

### **Variáveis de Ambiente**

Para configurar cache ou outras opções:
```toml
SOCCERDATA_DIR = "/tmp/soccerdata"
SOCCERDATA_LOGLEVEL = "INFO"
```

---

## 📊 **Limites do Streamlit Cloud (Free Tier)**

| Recurso | Limite |
|---------|--------|
| **Apps** | 1 app privado ou unlimited públicos |
| **CPU** | 1 CPU |
| **RAM** | 1 GB |
| **Storage** | Efémero (reinicia ao redeployar) |
| **Uptime** | 24/7 (com sleeps após inatividade) |

**⚠️ Nota:** App entra em sleep após ~7 dias sem uso. Acorda automaticamente quando alguém acede.

---

## 🐛 **Troubleshooting**

### **Problema: Deploy falha**
**Soluções:**
1. Verificar `requirements.txt` tem todas as dependências
2. Ver logs no Streamlit Cloud
3. Testar localmente: `streamlit run streamlit_app.py`

### **Problema: Timeout no carregamento de dados**
**Soluções:**
1. Reduzir número de temporadas
2. Usar menos ligas
3. Aumentar TTL do cache
4. Considerar upgrade para plano pago

### **Problema: App muito lenta**
**Soluções:**
1. Limitar dados exibidos (já usa TOP 100)
2. Otimizar queries Polars
3. Usar st.cache_data mais agressivamente

### **Problema: Out of Memory**
**Soluções:**
1. Processar dados em chunks
2. Remover colunas não usadas mais cedo
3. Usar dtypes mais eficientes

---

## 🚀 **Comandos Git Úteis**

```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Commit
git commit -m "Mensagem descritiva"

# Push para GitHub
git push

# Ver histórico
git log --oneline

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1
```

**Nota:** Cada push para `main` faz redeploy automático!

---

## 📈 **Melhorias Futuras**

Para apps em produção:
- [ ] Adicionar autenticação (st.experimental_user)
- [ ] Logging para monitorização
- [ ] Rate limiting para APIs
- [ ] Backup de dados
- [ ] Analytics (Google Analytics)
- [ ] Dark mode toggle
- [ ] Multi-idioma (i18n)

---

## 🎯 **Checklist Pré-Deploy**

Antes de fazer deploy:
- [x] `requirements.txt` criado
- [x] `.streamlit/config.toml` criado
- [x] `.gitignore` atualizado
- [x] Cache configurado (TTL)
- [x] Try-catch em load_data()
- [x] README.md atualizado
- [ ] Testar localmente
- [ ] Repositório GitHub criado
- [ ] Push para GitHub
- [ ] Deploy no Streamlit Cloud

---

## 📞 **Links Úteis**

- **Streamlit Cloud**: https://share.streamlit.io
- **Documentação Deploy**: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- **Community Forum**: https://discuss.streamlit.io
- **Status Page**: https://status.streamlit.io

---

## 💡 **Dicas de Otimização**

### **1. Cache Agressivo**
```python
@st.cache_data(ttl=86400)  # 24 horas
def expensive_computation():
    ...
```

### **2. Lazy Loading**
```python
if st.button("Carregar dados"):
    data = load_data()
```

### **3. Pagination**
```python
page = st.number_input("Página", 1, 10)
df_page = df.iloc[(page-1)*100:page*100]
```

### **4. Async/Background Jobs**
```python
import asyncio
async def fetch_data():
    ...
```

---

## 🎓 **Tutorial Vídeo (Conceitual)**

1. **Login GitHub** → https://github.com
2. **New Repository** → público
3. **Git push** → código vai para GitHub
4. **Streamlit Cloud** → https://share.streamlit.io
5. **New App** → selecionar repo
6. **Deploy** → aguardar 5-10 min
7. **Share URL** → app público!

---

**Pronto para Deploy! 🚀**

Qualquer dúvida, consultar documentação oficial do Streamlit ou GitHub.
