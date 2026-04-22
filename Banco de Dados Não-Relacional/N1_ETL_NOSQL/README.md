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

### Dependências Python

Todas as dependências estão em `backend/requirements.txt` e são instaladas automaticamente pelo Docker:

- `fastapi` — framework web
- `uvicorn` — servidor ASGI
- `pandas` — manipulação de dados
- `pymongo` — driver MongoDB
- `psycopg2-binary` — driver PostgreSQL
- `httpx` — cliente HTTP
- `python-dotenv` — carregamento de variáveis de ambiente

Para instalar localmente sem Docker: `pip install -r backend/requirements.txt`

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

### Health & Infraestrutura

| Método | Rota | Descrição | Resposta |
|---|---|---|---|
| `GET` | `/health` | Status da API, MongoDB e PostgreSQL | `{"status": "ok", "api": "online", "mongodb": "connected", "postgresql": "connected"}` |

### Pipeline

| Método | Rota | Descrição | Parâmetros |
|---|---|---|---|
| `POST` | `/pipeline/bd-producao-artistica` | Executa a pipeline ETL completa com os 3 JSONL | Recebe 3 arquivos: `producao`, `pessoa`, `equipe` |
| `POST` | `/pipeline/upload` | Upload de CSV e execução da pipeline | Arquivo CSV no body; opcional: `collection_name` |
| `POST` | `/pipeline/url` | Importação por URL pública e execução | `url` (string), `collection_name` (opcional) |

### Analytics — Consultas Simples

| Método | Rota | Descrição | O que retorna |
|---|---|---|---|
| `GET` | `/analytics/summary` | Total de registros e última ingestão | Total de documentos e timestamp UTC da última atualização |
| `GET` | `/analytics/quality-report` | Último relatório de qualidade gerado | Estatísticas pré-transformação: nulos, duplicatas, outliers, completude |
| `GET` | `/analytics/datasets` | Lista todos os datasets ingeridos | Array de datasets com `collection_name`, `record_count`, `source`, `timestamp` |

### Analytics — Agregações e Rankings (3 JSONL)

| Método | Rota | Descrição | Exemplo de Resultado |
|---|---|---|---|
| `GET` | `/analytics/bd/producoes-por-ano` | Distribuição de produções por ano (agregação) | `[{"_id": 2020, "count": 45}, {"_id": 2021, "count": 67}, ...]` |
| `GET` | `/analytics/bd/producoes-por-tipo` | Distribuição por tipo de produção (agregação) | `[{"tipo": "Teatro", "count": 120}, {"tipo": "Cinema", "count": 85}, ...]` |
| `GET` | `/analytics/bd/ranking-pessoas` | Top 20 pessoas com mais participações (ranking) | `[{"pessoa_id": "123", "nome": "João Silva", "participacoes": 15}, ...]` |
| `GET` | `/analytics/bd/papeis-mais-frequentes` | Papéis mais frequentes na equipe (agregação) | `[{"papel": "Diretor", "frequencia": 234}, {"papel": "Ator", "frequencia": 512}, ...]` |

### Analytics — Comparação MongoDB vs PostgreSQL

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/analytics/comparacao-sql` | Comparação de contagens entre MongoDB e PostgreSQL (valida integridade dos dados espelhados) |

**Documentação interativa completa**: http://localhost:8000/docs

---

## Collections MongoDB Criadas

| Collection | Camada | Descrição | Uso |
|---|---|---|---|
| `raw_producao` | RAW | Dados brutos de produção (sem tratamento) | Auditoria; comparação com dados transformados |
| `raw_pessoa` | RAW | Dados brutos de pessoas | Auditoria; comparação com dados transformados |
| `raw_equipe` | RAW | Dados brutos de equipe | Auditoria; comparação com dados transformados |
| `producao_clean` | CLEAN | Produções tratadas (upsert por hash) | Base para enriquecimento |
| `pessoa_clean` | CLEAN | Pessoas tratadas | Base para enriquecimento |
| `equipe_clean` | CLEAN | Equipe tratada | Base para enriquecimento |
| `producoes_com_participantes` | RICH | Produções com participantes aninhados (principal) | **Coleção de consumo para analytics e frontend** |
| `quality_reports` | META | Relatórios de qualidade gerados pela pipeline | Histórico de qualidade dos dados; endpoint `/analytics/quality-report` |
| `datasets_index` | META | Índice de datasets ingeridos | Rastreamento de uploads e URLs importadas |

> **Dica**: Use `producoes_com_participantes` para todas as queries analíticas — é a coleção final enriquecida com dados completos.

---

## Campos ETL Adicionados

Cada registro nas coleções CLEAN e RICH recebe automaticamente:

| Campo | Descrição | Exemplo |
|---|---|---|
| `_etl_source` | Origem: `"csv"`, `"url"` ou `"jsonl"` | `"jsonl"` |
| `_etl_timestamp` | Data/hora da ingestão (ISO 8601 UTC) | `"2024-04-22T14:32:15Z"` |
| `_etl_filename` | Nome do arquivo ou URL de origem | `"producao.jsonl"` ou `"https://exemplo.com/dados.csv"` |
| `_hash` | Hash SHA-256 do registro (chave de deduplicação) | `"a3f5e8c2d1b4..."` |
| `_created_at` | Data/hora da primeira inserção no MongoDB | `"2024-04-22T14:32:15Z"` |

---

## Entendendo o Quality Report

O **Quality Report** é gerado na etapa 2 da pipeline e oferece visibilidade dos dados **antes** de qualquer transformação:

- **Nulos (Missing)**: Campos com valores ausentes
- **Duplicatas**: Registros completamente duplicados
- **Outliers**: Valores numéricos muito desviados da média (Interquartile Range)
- **Completude**: Percentual de campos preenchidos por coluna
- **Estatísticas Descritivas**: Min, max, média, mediana para campos numéricos

Acesse via: **GET `/analytics/quality-report`** ou use o frontend (aba **Pipeline BD** → relatório após executar).

> **Uso**: Identifique problemas nos dados brutos para ajustar as transformações se necessário.

---

## Documentação Complementar

O projeto inclui 3 documentos técnicos em `docs/`:

- **[comparacao_sql.md](docs/comparacao_sql.md)** — Análise MongoDB vs PostgreSQL (Etapa 6): schemas, queries, vantagens de cada modelo
- **[decisoes_tecnicas.md](docs/decisoes_tecnicas.md)** — Justificativas de arquitetura, escolhas de tecnologias, design patterns
- **[problemas_encontrados.md](docs/problemas_encontrados.md)** — Problemas identificados no BD_Producao_Artistica (data quality, inconsistências)

Consulte esses arquivos para entender decisões de design e limitações conhecidas.

---

## Logs e Debugging

### Ver Logs do Backend (FastAPI)

```bash
# Logs em tempo real
docker compose logs -f backend

# Últimas 100 linhas
docker compose logs backend --tail 100

# Apenas erros
docker compose logs backend | grep -i error
```

### Ver Logs do MongoDB

```bash
docker compose logs -f mongo
```

### Ver Logs do PostgreSQL

```bash
docker compose logs -f postgres
```

### Console do Frontend

1. Acesse http://localhost:3000
2. Abra DevTools: **F12** ou **Ctrl+Shift+I**
3. Clique na aba **Console** para ver erros de JavaScript

### Acessar MongoDB via Shell

```bash
# Conectar ao container
docker exec -it etl_mongo mongosh --authenticationDatabase admin etl_db

# Listar coleções
show collections

# Ver qualidade mais recente
db.quality_reports.findOne(sort: {_etl_timestamp: -1})
```

### Acessar PostgreSQL via Shell

```bash
# Conectar ao container
docker exec -it etl_postgres psql -U etl_user -d etl_db

# Listar tabelas
\dt

# Contar registros
SELECT COUNT(*) FROM producao_clean;
```

---

## Troubleshooting

### Container não inicia

**Sintoma**: `docker compose up` falha com erro de porta ocupada ou build failure

**Solução**:
```bash
# Limpar completamente
docker compose down -v
docker system prune -a

# Rebuildar do zero
docker compose up --build
```

### MongoDB não conecta

**Sintoma**: `"mongodb": "unreachable"` no `/health`

**Verificar**:
```bash
# Ver se o container está rodando
docker ps | grep mongo

# Checar logs
docker compose logs mongo

# Verificar conectividade
docker exec etl_backend curl -s http://mongo:27017 2>&1 || echo "Conexão falhou"
```

### PostgreSQL não conecta

**Sintoma**: `"postgresql": "unreachable"` no `/health`

**Verificar**:
```bash
docker ps | grep postgres
docker compose logs postgres
```

### Pipeline falha com "collection already exists"

**Sintoma**: Executar pipeline 2x resulta em erro

**Solução**: MongoDB não permite recriar coleções. Isso é esperado — a segunda execução faz upsert (atualiza registros existentes via hash). Se quiser resetar:
```bash
docker compose down -v
```

### Frontend não carrega, botão não responde

**Sintoma**: http://localhost:3000 carrega mas botões não funcionam

**Solução**:
1. Abra em modo anônimo do navegador (ad blockers podem bloquear requests)
2. Verifique DevTools (F12) → Console para erros JavaScript
3. Verifique se backend está respondendo: http://localhost:8000/health

### Dados aparecem em MongoDB mas não no Analytics

**Sintoma**: Collections criadas mas endpoints retornam vazio

**Verificar**:
- A pipeline foi executada até o fim (verifique `producoes_com_participantes`)?
- Há dados em `raw_*` mas não em `*_clean`? Pode ser erro na transformação — veja logs
- Dados em `*_clean` mas não em `producoes_com_participantes`? Erro no enrichment

```bash
# Verificar cada layer
docker exec etl_backend python -c "
from app.database.mongo import get_db
db = get_db()
print('RAW:', db.raw_producao.count_documents({}))
print('CLEAN:', db.producao_clean.count_documents({}))
print('RICH:', db.producoes_com_participantes.count_documents({}))
"
```

### OutOfMemory ou pipeline muito lenta

**Causa**: Datasets muito grandes ou transformações ineficientes

**Solução**:
- Processar em lotes menores
- Aumentar memória do Docker: `Settings → Resources → Memory`
- Consultar [decisoes_tecnicas.md](docs/decisoes_tecnicas.md) para ajustes recomendados

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
