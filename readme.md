# 🚀 Projeto Analytics Engineering - DBT + Airflow + PostgreSQL

Projeto de Analytics Engineering utilizando **DBT**, **Apache Airflow** e **PostgreSQL** em containers Docker, com ambiente de desenvolvimento local em Python.

---

## 📋 **Índice**

- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Iniciar o Projeto](#-como-iniciar-o-projeto)
- [Acessar as Interfaces](#-acessar-as-interfaces)
- [Comandos Úteis](#-comandos-úteis)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Troubleshooting](#-troubleshooting)

---

## 🏗️ **Arquitetura do Projeto**

### **Estrutura Simplificada:**

**AMBIENTE LOCAL (seu computador):**
- Python + DBT instalado no `.venv`
- Você desenvolve modelos SQL no VS Code
- DBT conecta ao PostgreSQL via `localhost:5432`

**DOCKER (containers isolados):**
- **PostgreSQL** - Banco de dados (porta 5432)
- **Airflow** - Orquestrador de pipelines (porta 8080)
- **PgAdmin** - Interface web para ver dados (porta 5050)

### **Como funciona:**

1. Você escreve modelos DBT localmente (arquivos `.sql`)
2. Executa `dbt run` no terminal
3. DBT conecta ao PostgreSQL no Docker
4. Tabelas são criadas no database `analytics`
5. Airflow pode agendar execuções automáticas do DBT
6. PgAdmin permite visualizar os dados criados

### **Componentes:**

| Componente | Localização | Porta | Função |
|------------|-------------|-------|--------|
| **DBT** | Local (.venv) | - | Transformação de dados (ELT) |
| **PostgreSQL** | Docker | 5432 | Banco de dados principal |
| **Airflow Webserver** | Docker | 8080 | Interface web do Airflow |
| **Airflow Scheduler** | Docker | - | Agendador de tarefas |
| **PgAdmin** | Docker | 5050 | Interface web para PostgreSQL |

### **Acessos:**

| Interface | URL | Credenciais |
|-----------|-----|-------------|
| **Airflow** | http://localhost:8080 | admin / admin |
| **PgAdmin** | http://localhost:5050 | admin@admin.com / admin123 |
| **PostgreSQL** | localhost:5432 | airflow / airflow123 |

---

## 📦 **Pré-requisitos**

Antes de iniciar, certifique-se de ter instalado:

### **Obrigatórios:**

| Software | Versão Mínima | Link |
|----------|---------------|------|
| **Python** | 3.10+ | [Download](https://www.python.org/downloads/) |
| **Docker Desktop** | 24.x+ | [Download](https://www.docker.com/products/docker-desktop/) |
| **Git** | 2.x+ | [Download](https://git-scm.com/downloads) |
| **VS Code** | Última | [Download](https://code.visualstudio.com/) |

### **Verificar instalações:**

```bash
# Verificar Python
python --version

# Verificar Docker
docker --version

# Verificar Docker Compose
docker-compose --version

# Verificar Git
git --version
```

---

## 🛠️ **Instalação e Configuração**

### **PASSO 1: Clonar o repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd projeto_dbt
```

---

### **PASSO 2: Criar e ativar ambiente virtual Python**

**Windows (PowerShell):**
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

**Você deve ver `(.venv)` no início da linha do terminal.**

---

### **PASSO 3: Instalar dependências Python**

```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação do DBT
dbt --version
```

**Saída esperada:**
```
Core:
  - installed: 1.7.4
Plugins:
  - postgres: 1.7.4
```

---

### **PASSO 4: Configurar variáveis de ambiente**

Copie o arquivo `.env.example` para `.env`:

**Windows:**
```powershell
Copy-Item .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

**Edite o arquivo `.env` e altere as senhas se necessário.**

---

### **PASSO 5: Iniciar Docker Desktop**

1. Abra o **Docker Desktop**
2. Aguarde até que o Docker esteja rodando (ícone verde)
3. Verifique no terminal:

```bash
docker ps
```

---

### **PASSO 6: Subir os containers Docker**

```bash
# Navegar até a pasta docker
cd docker

# Subir todos os containers
docker-compose up -d

# Verificar status dos containers
docker-compose ps
```

**Saída esperada:**

| Nome | Status | Portas |
|------|--------|--------|
| projeto_dbt_postgres | Up (healthy) | 0.0.0.0:5432->5432/tcp |
| projeto_dbt_pgadmin | Up | 0.0.0.0:5050->80/tcp |
| projeto_dbt_airflow_webserver | Up | 0.0.0.0:8080->8080/tcp |
| projeto_dbt_airflow_scheduler | Up | - |

⏱️ **Tempo estimado:** 3-5 minutos (primeira vez pode demorar mais)

**Acompanhar os logs:**
```bash
docker-compose logs -f
```

---

### **PASSO 7: Criar usuário admin do Airflow**

```bash
docker exec -it projeto_dbt_airflow_webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

**Verificar:**
```bash
docker exec -it projeto_dbt_airflow_webserver airflow users list
```

---

### **PASSO 8: Criar database analytics no PostgreSQL**

```bash
# Conectar ao PostgreSQL
docker exec -it projeto_dbt_postgres psql -U airflow -d airflow

# Dentro do PostgreSQL, executar:
CREATE DATABASE analytics;

# Verificar que foi criado
\l

# Sair
\q
```

---

### **PASSO 9: Configurar DBT**

```bash
# Voltar para a raiz do projeto
cd ..

# Ativar ambiente virtual (se não estiver ativo)
# Windows: .venv\Scripts\activate
# Linux/Mac: source .venv/bin/activate

# Navegar até o projeto DBT
cd dbt_project

# Testar conexão
dbt debug
```

**Saída esperada:**
```
Connection test: [OK connection ok]
All checks passed!
```

---

### **PASSO 10: Executar modelos DBT de exemplo**

```bash
# Executar modelos
dbt run

# Executar testes
dbt test
```

**Saída esperada:**
```
Completed successfully
Done. PASS=2 WARN=0 ERROR=0 SKIP=0 TOTAL=2
```

---

## 🌐 **Acessar as Interfaces**

### **1. Airflow - Orquestração de Workflows**

- **URL:** http://localhost:8080
- **Usuário:** `admin`
- **Senha:** `admin`
- **Descrição:** Interface para criar, agendar e monitorar DAGs (pipelines de dados)

### **2. PgAdmin - Gerenciamento do PostgreSQL**

- **URL:** http://localhost:5050
- **Email:** `admin@admin.com`
- **Senha:** `admin123`
- **Descrição:** Interface web para visualizar e gerenciar bancos de dados PostgreSQL

**Configurar conexão no PgAdmin:**

1. Clique em **Add New Server**
2. **Aba General:**
   - Name: `Projeto DBT PostgreSQL`
3. **Aba Connection:**
   - Host: `postgres`
   - Port: `5432`
   - Maintenance database: `airflow`
   - Username: `airflow`
   - Password: `airflow123`
   - ✅ Marque: **Save password**
4. Clique em **Save**

### **3. PostgreSQL - Acesso direto via terminal**

```bash
# Conectar ao database analytics
docker exec -it projeto_dbt_postgres psql -U airflow -d analytics
```

**Comandos úteis:**

| Comando | Descrição |
|---------|-----------|
| `\l` | Listar databases |
| `\dt` | Listar tabelas |
| `\d+ <table>` | Descrever estrutura da tabela |
| `SELECT * FROM <table> LIMIT 10;` | Ver dados |
| `\q` | Sair |

---

## 🔧 **Comandos Úteis**

### **Docker:**

```bash
# Ver status dos containers
docker-compose ps

# Ver logs de todos os containers
docker-compose logs -f

# Ver logs de um container específico
docker-compose logs -f airflow-webserver

# Parar todos os containers
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Reiniciar um container específico
docker-compose restart airflow-webserver

# Reconstruir imagens
docker-compose build --no-cache

# Subir novamente
docker-compose up -d
```

### **DBT:**

```bash
# Testar conexão
dbt debug

# Executar todos os modelos
dbt run

# Executar modelo específico
dbt run --select my_first_dbt_model

# Executar modelos de uma pasta
dbt run --select staging.*

# Executar testes
dbt test

# Gerar documentação
dbt docs generate

# Servir documentação (abre no navegador)
dbt docs serve

# Limpar arquivos compilados
dbt clean

# Compilar sem executar
dbt compile
```

### **Airflow:**

```bash
# Listar DAGs
docker exec -it projeto_dbt_airflow_webserver airflow dags list

# Listar usuários
docker exec -it projeto_dbt_airflow_webserver airflow users list

# Pausar DAG
docker exec -it projeto_dbt_airflow_webserver airflow dags pause <dag_id>

# Despausar DAG
docker exec -it projeto_dbt_airflow_webserver airflow dags unpause <dag_id>
```

---

## 📁 **Estrutura do Projeto**

```
projeto_dbt/
├── .venv/                          # Ambiente virtual Python (NÃO versionar)
├── .vscode/                        # Configurações do VS Code
│   └── settings.json
├── docker/                         # Configurações Docker
│   ├── airflow/
│   │   ├── Dockerfile              # Imagem customizada do Airflow
│   │   └── requirements.txt        # Dependências Python do Airflow
│   └── docker-compose.yml          # Orquestração dos containers
├── airflow/                        # Código Airflow
│   ├── dags/                       # DAGs do Airflow
│   ├── logs/                       # Logs (NÃO versionar)
│   └── plugins/                    # Plugins customizados
├── dbt_project/                    # Projeto DBT
│   ├── analyses/                   # Queries SQL para análises
│   ├── macros/                     # Funções reutilizáveis
│   ├── models/                     # Modelos SQL
│   │   ├── staging/                # Camada de staging
│   │   ├── intermediate/           # Camada intermediária
│   │   └── marts/                  # Camada de marts
│   ├── seeds/                      # Arquivos CSV
│   ├── snapshots/                  # Capturas históricas
│   ├── tests/                      # Testes customizados
│   ├── target/                     # Compilados (NÃO versionar)
│   ├── logs/                       # Logs (NÃO versionar)
│   └── dbt_project.yml             # Configuração do projeto
├── scripts/                        # Scripts auxiliares
├── .env                            # Variáveis de ambiente (NÃO versionar)
├── .env.example                    # Template (versionar)
├── .gitignore                      # Arquivos ignorados
├── requirements.txt                # Dependências Python locais
└── README.md                       # Este arquivo
```

### **O que NÃO deve ser versionado:**

| Item | Motivo |
|------|--------|
| `.venv/` | Ambiente virtual (cada dev cria o seu) |
| `.env` | Contém credenciais |
| `__pycache__/` | Cache Python |
| `dbt_project/target/` | Arquivos compilados DBT |
| `dbt_project/logs/` | Logs DBT |
| `airflow/logs/` | Logs Airflow |
| `*.csv` (grandes) | Dados não devem ser versionados |

---

## 🐛 **Troubleshooting**

### **Problema 1: Containers não sobem**

**Sintoma:**
```
ERROR: Cannot start service postgres: port is already allocated
```

**Solução:**
```bash
# Windows:
netstat -ano | findstr :5432

# Linux/Mac:
lsof -i :5432

# Parar o processo ou mudar a porta no docker-compose.yml
```

---

### **Problema 2: DBT não conecta ao PostgreSQL**

**Sintoma:**
```
Connection test: [ERROR]
```

**Solução:**
```bash
# Verificar se PostgreSQL está rodando
docker ps | grep postgres

# Testar conexão direta
docker exec -it projeto_dbt_postgres psql -U airflow -d analytics

# Verificar profiles.yml
cat ~/.dbt/profiles.yml
```

---

### **Problema 3: Senha do Airflow não funciona**

**Sintoma:**
```
Login Failed for user: admin
```

**Solução:**
```bash
# Deletar e recriar o usuário
docker exec -it projeto_dbt_airflow_webserver airflow users delete --username admin

docker exec -it projeto_dbt_airflow_webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
```

---

### **Problema 4: Git tentando versionar .venv**

**Sintoma:**
```
Changes to be committed:
  .venv/Lib/site-packages/...
```

**Solução:**
```bash
# Remover .venv do staging
git reset
git rm -r --cached .venv

# Verificar .gitignore
cat .gitignore | grep ".venv"

# Adicionar novamente (respeitando .gitignore)
git add .
```

---

## 🔄 **Como Reiniciar o Projeto**

### **Reinício Completo (preserva dados):**

```bash
# Parar containers
cd docker
docker-compose down

# Subir novamente
docker-compose up -d
```

### **Reinício Limpo (apaga todos os dados):**

```bash
# Parar e remover volumes
cd docker
docker-compose down -v

# Subir novamente
docker-compose up -d

# Recriar usuário admin
docker exec -it projeto_dbt_airflow_webserver airflow users create \
  --username admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin

# Recriar database analytics
docker exec -it projeto_dbt_postgres psql -U airflow -d airflow -c "CREATE DATABASE analytics;"
```

---

## 📚 **Recursos Adicionais**

| Recurso | Link |
|---------|------|
| **DBT Documentation** | https://docs.getdbt.com/ |
| **Apache Airflow Documentation** | https://airflow.apache.org/docs/ |
| **PostgreSQL Documentation** | https://www.postgresql.org/docs/ |
| **Docker Documentation** | https://docs.docker.com/ |

---

## 👥 **Contribuindo**

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## ✨ **Autor**

**Andre Luiz** - Analytics Engineer

---

**🎉 Projeto configurado com sucesso! Happy coding!**