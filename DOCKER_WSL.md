# 🐳 Docker no WSL Ubuntu - Guia Completo

## 📋 Pré-requisitos

### 1. Instalar Docker no WSL Ubuntu

```bash
# Atualizar pacotes
sudo apt update

# Instalar Docker
sudo apt install docker.io -y

# Adicionar seu usuário ao grupo docker (evita usar sudo)
sudo usermod -aG docker $USER

# Aplicar mudanças de grupo
newgrp docker

# Iniciar Docker
sudo service docker start

# Verificar instalação
docker --version
```

### 2. Configurar Docker para iniciar automaticamente

```bash
# Adicionar ao ~/.bashrc para iniciar Docker automaticamente
echo '# Iniciar Docker automaticamente' >> ~/.bashrc
echo 'if ! docker info &> /dev/null; then' >> ~/.bashrc
echo '    sudo service docker start &> /dev/null' >> ~/.bashrc
echo 'fi' >> ~/.bashrc

# Recarregar ~/.bashrc
source ~/.bashrc
```

### 3. Instalar Docker Compose (opcional, mas recomendado)

```bash
# Instalar docker-compose
sudo apt install docker-compose -y

# Verificar instalação
docker-compose --version
```

## 🚀 Como Usar

### Opção 1: Scripts Automatizados (Recomendado)

#### 1. Dar permissão de execução aos scripts

```bash
chmod +x docker-build.sh docker-run.sh docker-stop.sh
```

#### 2. Build da imagem

```bash
./docker-build.sh
```

#### 3. Executar o container

```bash
./docker-run.sh
```

#### 4. Acessar o dashboard

Abra seu navegador em: **http://localhost:8501**

#### 5. Parar o container

```bash
./docker-stop.sh
```

### Opção 2: Docker Compose Manual

#### 1. Build

```bash
sudo docker-compose build
```

#### 2. Executar

```bash
sudo docker-compose up -d
```

#### 3. Ver logs

```bash
sudo docker-compose logs -f
```

#### 4. Parar

```bash
sudo docker-compose down
```

### Opção 3: Docker Direto (sem compose)

#### 1. Build

```bash
sudo docker build -t soccerdata-dashboard .
```

#### 2. Executar

```bash
sudo docker run -d \
    --name soccerdata-dashboard \
    -p 8501:8501 \
    -v $(pwd)/cache:/app/cache \
    --restart unless-stopped \
    soccerdata-dashboard
```

#### 3. Ver logs

```bash
sudo docker logs -f soccerdata-dashboard
```

#### 4. Parar

```bash
sudo docker stop soccerdata-dashboard
sudo docker rm soccerdata-dashboard
```

## 🔧 Comandos Úteis

### Ver containers rodando

```bash
sudo docker ps
```

### Ver todas as imagens

```bash
sudo docker images
```

### Ver logs do container

```bash
sudo docker logs -f soccerdata-dashboard
```

### Entrar no container (shell interativo)

```bash
sudo docker exec -it soccerdata-dashboard bash
```

### Remover imagens não utilizadas

```bash
sudo docker system prune -a
```

### Rebuild forçado (ignorar cache)

```bash
sudo docker-compose build --no-cache
```

### Ver uso de recursos

```bash
sudo docker stats soccerdata-dashboard
```

## 🐛 Troubleshooting

### Erro: "Cannot connect to the Docker daemon"

```bash
# Iniciar Docker
sudo service docker start

# Verificar status
sudo service docker status
```

### Erro: "permission denied"

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Ou usar sudo nos comandos
sudo docker ps
```

### Porta 8501 já está em uso

```bash
# Ver o que está usando a porta
sudo lsof -i :8501

# Ou mudar a porta no docker-compose.yml
# De: "8501:8501"
# Para: "8502:8501"
# Depois acessar: http://localhost:8502
```

### Container não inicia

```bash
# Ver logs de erro
sudo docker logs soccerdata-dashboard

# Verificar se a imagem foi construída
sudo docker images | grep soccerdata

# Rebuild
./docker-build.sh
```

### Dados não estão sendo salvos

```bash
# Verificar se o diretório cache existe
mkdir -p cache

# Verificar volumes montados
sudo docker inspect soccerdata-dashboard | grep -A 10 Mounts
```

### WSL não inicia Docker automaticamente

```bash
# Adicionar ao ~/.bashrc
nano ~/.bashrc

# Adicionar no final:
if ! docker info &> /dev/null; then
    sudo service docker start &> /dev/null
fi

# Salvar e recarregar
source ~/.bashrc
```

## 📦 Volumes e Persistência

O projeto usa volumes para persistir dados:

- `./cache:/app/cache` - Cache de dados do soccerdata (persiste entre restarts)
- `./streamlit_app.py:/app/streamlit_app.py` - Hot reload do código (desenvolvimento)
- `./app.py:/app/app.py` - Hot reload do código (desenvolvimento)

**Nota**: Os volumes de código permitem editar `streamlit_app.py` e `app.py` sem rebuild, mas você precisará recarregar a página no navegador.

## ⚙️ Configurações Avançadas

### Modo de Desenvolvimento

No `docker-compose.yml`, os volumes de código estão ativados por padrão:

```yaml
volumes:
  - ./cache:/app/cache
  - ./streamlit_app.py:/app/streamlit_app.py  # <- desenvolvimento
  - ./app.py:/app/app.py                        # <- desenvolvimento
```

### Modo de Produção

Para produção, comente os volumes de código:

```yaml
volumes:
  - ./cache:/app/cache
  # - ./streamlit_app.py:/app/streamlit_app.py  # <- comentado
  # - ./app.py:/app/app.py                        # <- comentado
```

### Variáveis de Ambiente

Você pode adicionar variáveis de ambiente no `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_HEADLESS=true
  # Adicione suas variáveis aqui
```

## 🌐 Acessar de Outro Computador na Rede

Por padrão, o dashboard está acessível apenas em `localhost:8501`.

Para acessar de outro computador:

1. Descobrir o IP do seu WSL:

```bash
ip addr show eth0 | grep inet
```

2. Acessar de outro computador na mesma rede:

```
http://SEU_IP_WSL:8501
```

**Nota**: O Windows Firewall pode bloquear. Você pode precisar adicionar uma regra de exceção.

## 📚 Recursos Adicionais

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 💡 Dicas

1. **Use docker-compose** para desenvolvimento - é mais fácil gerenciar
2. **Ative hot reload** mantendo os volumes de código montados
3. **Use `sudo docker logs -f`** para ver erros em tempo real
4. **Faça backup do diretório `cache/`** se tiver dados importantes
5. **Use `docker system prune`** ocasionalmente para limpar espaço

---

**✅ Pronto!** Agora você pode desenvolver e testar localmente no WSL Ubuntu com Docker.
