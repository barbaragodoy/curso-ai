# ETL BD Produção Artística

Pipeline ETL completa para leitura, tratamento e armazenamento de dados do dataset **BD_Producao_Artistica** no MongoDB, com comparação relacional no PostgreSQL, frontend web para operação visual e dashboard analítico.

---

## Visão Geral da Arquitetura

```
┌──────────────────────────────────────────────────────────────┐
│                      FRONTEND (Nginx :3000)                  │
│  ┌─────────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │  Pipeline BD     │  │  Upload CSV  │  │  Analytics     │  │
│  │  (3 JSONL)       │  │  / URL       │  │  Dashboard     │  │
│  └────────┬─────────┘  └──────┬───────┘  └───────┬────────┘  │
└───────────┼───────────────────┼──────────────────┼───────────┘
            │        HTTP/REST  │                  │
┌───────────▼───────────────────▼──────────────────▼───────────┐
│                     BACKEND (FastAPI :8000)                   │
│                                                               │
│  ┌──────────┐  ┌─────────────┐  ┌───────────────────────┐   │
│  │ Extractor│→ │Quality Check│→ │      Transformer       │   │
│  │CSV/JSONL │  │ (pré-transf)│  │limpeza + tipagem + meta│   │
│  └──────────┘  └─────────────┘  └───────────┬───────────┘   │
│                                              │                │
│                                   ┌──────────▼─────────┐     │
│                                   │  Loader (upsert)   │     │
│                                   └──────────┬─────────┘     │
│                                              │                │
│                                   ┌──────────▼─────────┐     │
│                                   │  Enricher          │     │
│                                   │  (join 3 datasets) │     │
│                                   └──────────┬─────────┘     │
└──────────────────────────────────────────────┼───────────────┘
                            ┌───────────────────┴──────────────┐
               ┌────────────▼──────────┐   ┌───────────────────▼──┐
               │      MongoDB 7        │   │    PostgreSQL 16      │
               │  (banco principal)    │   │  (comparação SQL)     │
               └───────────────────────┘   └──────────────────────┘
```

---

## Fluxo da Pipeline Principal (3 JSONL)

1. **Extract** — lê os 3 arquivos JSONL (`produção.jsonl`, `pessoa.jsonl`, `equipe.jsonl`)
2. **Quality Check** — gera relatório de qualidade pré-tratamento (nulos, duplicatas, outliers, completude) e salva no MongoDB
3. **RAW Load** — insere os dados brutos em `raw_producao`, `raw_pessoa`, `raw_equipe` (sem modificação)
4. **Transform** — normaliza colunas (snake_case), remove duplicatas, converte datas para ISO 8601, coerce tipos numéricos, preenche nulos, adiciona campos `_etl_*`
5. **CLEAN Load** — upsert via hash SHA-256 em `producao_clean`, `pessoa_clean`, `equipe_clean`
6. **Enrichment** — junta os 3 datasets em `producoes_com_participantes` com participantes aninhados por produção
7. **PostgreSQL Mirror** — espelha os dados tratados no PostgreSQL para comparação relacional (Etapa 6)

---

## Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) 24+
- [Docker Compose](https://docs.docker.com/compose/) v2+

```bash
docker --version
docker compose version
```

---

## Como Rodar

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/etl-bd-producao-artistica.git
cd etl-bd-producao-artistica
```

### 2. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

O `.env` padrão já funciona para rodar localmente com Docker. Edite apenas se quiser usar MongoDB Atlas ou outro banco externo.

### 3. Subir os containers

```bash
docker compose up --build
```

Aguarde até ver `Application startup complete` no log do backend.

### 4. Acessar

| Serviço | URL |
|---|---|
| Frontend | http://localhost:3000 |
| API — Swagger (docs interativos) | http://localhost:8000/docs |
| API — ReDoc | http://localhost:8000/redoc |
| API — Health check | http://localhost:8000/health |
| MongoDB | localhost:27017 |
| PostgreSQL | localhost:5432 |

### 5. Resetar (apagar todos os dados)

```bash
docker compose down -v   # remove containers + volumes
docker compose up --build
```

---

## Como Usar o Frontend

### Pipeline BD — JSONL (principal)

1. Acesse http://localhost:3000
2. Na aba **Pipeline BD**, clique em cada slot e selecione o arquivo correspondente:
   - `produção.jsonl` → slot **produção.jsonl**
   - `pessoa.jsonl` → slot **pessoa.jsonl**
   - `equipe.jsonl` → slot **equipe.jsonl**
3. Após selecionar os **3 arquivos**, o botão **▶ Executar Pipeline Completa** ficará ativo
4. Clique no botão e aguarde o processamento
5. O resultado exibe: relatório de qualidade, collections criadas, enriquecimento e status do PostgreSQL

> **Importante:** use uma aba anônima do browser se o botão não responder — extensões como ad blockers podem bloquear o envio do formulário.

### Upload de CSV

1. Clique na aba **Upload CSV**
2. Arraste ou selecione um arquivo `.csv`
3. Clique em **Executar Pipeline**

### Importar por URL

1. Clique na aba **Importar URL**
2. Cole a URL do arquivo público
3. Clique em **Importar e Executar Pipeline**

URLs suportadas: CSV direto, Google Sheets, JSON público.

### Analytics

1. Clique na aba **Analytics**
2. O dashboard carrega automaticamente após a pipeline BD ser executada
3. Use **Atualizar** para recarregar após novas ingestões

---

## Endpoints da API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Status da API, MongoDB e PostgreSQL |
| `POST` | `/pipeline/bd-producao-artistica` | Pipeline completa com os 3 JSONL |
| `POST` | `/pipeline/upload` | Upload de CSV e execução da pipeline |
| `POST` | `/pipeline/url` | Importação por URL e execução da pipeline |
| `GET` | `/analytics/summary` | Total de registros e última ingestão |
| `GET` | `/analytics/bd/producoes-por-ano` | Distribuição de produções por ano |
| `GET` | `/analytics/bd/producoes-por-tipo` | Distribuição por tipo de produção |
| `GET` | `/analytics/bd/ranking-pessoas` | Top 20 pessoas com mais participações |
| `GET` | `/analytics/bd/papeis-mais-frequentes` | Papéis mais frequentes na equipe |
| `GET` | `/analytics/comparacao-sql` | Comparação MongoDB vs PostgreSQL |
| `GET` | `/analytics/quality-report` | Último relatório de qualidade |

Documentação interativa completa: http://localhost:8000/docs

---

## Collections MongoDB Criadas

| Collection | Camada | Descrição |
|---|---|---|
| `raw_producao` | RAW | Dados brutos de produção (sem tratamento) |
| `raw_pessoa` | RAW | Dados brutos de pessoas |
| `raw_equipe` | RAW | Dados brutos de equipe |
| `producao_clean` | CLEAN | Produções tratadas (upsert por hash) |
| `pessoa_clean` | CLEAN | Pessoas tratadas |
| `equipe_clean` | CLEAN | Equipe tratada |
| `producoes_com_participantes` | RICH | Produções com participantes aninhados (principal) |
| `quality_reports` | META | Relatórios de qualidade gerados pela pipeline |
| `datasets_index` | META | Índice de datasets ingeridos |

---

## Campos ETL Adicionados

Cada registro nas coleções CLEAN recebe automaticamente:

| Campo | Descrição |
|---|---|
| `_etl_source` | Origem: `"csv"`, `"url"` ou `"jsonl"` |
| `_etl_timestamp` | Data/hora da ingestão (ISO 8601 UTC) |
| `_etl_filename` | Nome do arquivo ou URL de origem |
| `_hash` | Hash SHA-256 do registro (chave de deduplicação) |
| `_created_at` | Data/hora da primeira inserção no MongoDB |

---

## Conexões com Ferramentas Externas

### MongoDB Compass

```
URI: mongodb://localhost:27017
```

### DBeaver / PostgreSQL

| Campo | Valor |
|---|---|
| Host | `localhost` |
| Porta | `5432` |
| Banco | `etl_db` |
| Usuário | `etl_user` |
| Senha | `etl_pass` |

---

## Configurar MongoDB Externo (opcional)

Edite o `.env` para usar MongoDB Atlas:

```
MONGODB_URI=mongodb+srv://usuario:senha@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=etl_db
```

Após alterar, reinicie os containers:

```bash
docker compose down && docker compose up --build
```

---

## Estrutura de Pastas

```
etl-bd-producao-artistica/
├── backend/
│   ├── app/
│   │   ├── config.py              # Variáveis de ambiente
│   │   ├── main.py                # FastAPI + CORS + routers
│   │   ├── database/
│   │   │   ├── mongo.py           # Conexão MongoDB (singleton)
│   │   │   └── postgres.py        # Conexão PostgreSQL + carga
│   │   ├── pipeline/
│   │   │   ├── extractor.py       # Extract: CSV, JSONL e URL
│   │   │   ├── quality.py         # Relatório de qualidade
│   │   │   ├── transformer.py     # Transformações e limpeza
│   │   │   ├── loader.py          # Upsert no MongoDB
│   │   │   └── enricher.py        # Join 3 datasets → producoes_com_participantes
│   │   └── routes/
│   │       ├── bd_pipeline.py     # POST /pipeline/bd-producao-artistica
│   │       ├── upload.py          # POST /pipeline/upload
│   │       ├── url_import.py      # POST /pipeline/url
│   │       └── analytics.py       # GET /analytics/*
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html                 # Interface principal
│   ├── style.css                  # Tema escuro
│   └── app.js                     # Lógica do frontend
├── docs/
│   ├── comparacao_sql.md          # MongoDB vs PostgreSQL (Etapa 6)
│   ├── decisoes_tecnicas.md       # Justificativas das escolhas do projeto
│   └── problemas_encontrados.md   # Problemas identificados na base de dados
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## Versionamento

```bash
git init
git add .
git commit -m "feat: pipeline ETL BD Producao Artistica"
git remote add origin https://github.com/SEU_USUARIO/etl-bd-producao-artistica.git
git branch -M main
git push -u origin main
```

> O arquivo `.env` está no `.gitignore` e **não será versionado**.
