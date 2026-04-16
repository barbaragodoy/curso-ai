# MongoDB Atlas - Atividade Prática

## Objetivo
Estabelecer conexão com MongoDB Atlas, inserir dados de teste (IMDB Top 1000), executar consultas, agregações e criar índices para otimização de banco de dados.

## Pré-requisitos

### 1. Instalar dependências Python
```bash
pip install pymongo pandas
```

### 2. Credenciais MongoDB Atlas
- **Username:** admin
- **Password:** admin
- **Cluster URI:** [CLUSTER_URL]
- **Database:** imdb
- **Collection:** movies

### 3. Arquivo de dados
- **Arquivo:** IMDB top 1000.csv
- **Localização:** Mesmo diretório dos scripts

## Estrutura dos arquivos

### 1. mongodb_operations.py
Script principal com operações básicas:
- Conexão ao MongoDB Atlas
- Inserção de dados do CSV
- Queries simples (por gênero, nota, certificado)
- Agregações (média por certificado, estatísticas por gênero)
- Criação de índices (simples e compostos)

### 2. advanced_queries.py
Script com operações avançadas:
- Consultas com filtros complexos
- Agregações com bucketing
- Análise de cast/atores
- Correlação de dados (Metascore vs Rate)
- Índices de texto e sparse
- Estatísticas da coleção

## Como executar

### Executar inserção e operações básicas
```bash
python mongodb_operations.py
```

**O que faz:**
1. Conecta ao MongoDB Atlas
2. Insere 1000 documentos do CSV
3. Executa 3 queries diferentes
4. Realiza 2 agregações
5. Cria 4 índices
6. Salva log em `mongodb_operations_log.txt`

### Executar consultas avançadas
```bash
python advanced_queries.py
```

**O que faz:**
1. Executa 5 consultas avançadas
2. Realiza 4 agregações complexas
3. Cria índices especiais
4. Obtém estatísticas
5. Salva resultados em `advanced_queries_results.txt`

## Operações detalhadas

### QUERIES (Consultas)

#### 1. Query por Gênero
```python
results = collection.find({"Genre": {"$regex": "Drama", "$options": "i"}})
```
- Busca filmes de um gênero específico
- Case-insensitive

#### 2. Query por Nota Mínima
```python
results = collection.find({"Rate": {"$gte": 8.8}})
```
- Filmes com nota maior ou igual a 8.8
- Ordenado decrescente

#### 3. Query por Classificação Etária
```python
count = collection.count_documents({"Certificate": "R"})
```
- Conta filmes com certificado específico
- Retorna quantidade

#### 4. Query por Texto
```python
results = collection.find({"Title": {"$regex": "war", "$options": "i"}})
```
- Busca por palavras no título
- Case-insensitive

#### 5. Query com Range de Ano
```python
results = collection.find({"Year": {"$gte": 2000, "$lte": 2020}})
```
- Filmes em intervalo de anos

### AGREGAÇÕES

#### 1. Média de nota por Certificado
```python
pipeline = [
    {"$group": {
        "_id": "$Certificate",
        "average_rate": {"$avg": "$Rate"},
        "count": {"$sum": 1}
    }},
    {"$sort": {"average_rate": -1}}
]
```
- Agrupa por certificado (G, PG, PG-13, R, etc)
- Calcula média de nota e contagem

#### 2. Estatísticas por Gênero
```python
pipeline = [
    {"$unwind": "$Genre"},
    {"$group": {
        "_id": "$Genre",
        "count": {"$sum": 1},
        "avg_rate": {"$avg": "$Rate"},
        "max_rate": {"$max": "$Rate"},
        "min_rate": {"$min": "$Rate"}
    }},
    {"$sort": {"avg_rate": -1}}
]
```
- Agrupa por gênero
- Calcula count, média, máximo e mínimo de notas

#### 3. Distribuição de Notas
```python
pipeline = [
    {"$bucket": {
        "groupBy": "$Rate",
        "boundaries": [0, 5, 6, 7, 8, 9, 10],
        "output": {"count": {"$sum": 1}}
    }}
]
```
- Agrupa filmes em faixas de nota
- Mostra quantidade em cada faixa

#### 4. Top Atores/Atrizes
```python
pipeline = [
    {"$project": {"actors": {"$split": ["$Cast", "|"]}}},
    {"$unwind": "$actors"},
    {"$group": {
        "_id": "$actors",
        "count": {"$sum": 1},
        "avg_rate": {"$avg": "$Rate"}
    }},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]
```
- Extrai atores do campo Cast
- Conta filmes por ator
- Calcula nota média

### ÍNDICES

#### 1. Índices Simples
```python
# Índice no campo Title
collection.create_index("Title")

# Índice no campo Rate
collection.create_index("Rate")

# Índice no campo Certificate
collection.create_index("Certificate")
```
- Acelera buscas por campo único
- Recomendado para campos muito consultados

#### 2. Índice Composto
```python
# Índice em Genre (asc) + Rate (desc)
collection.create_index([("Genre", 1), ("Rate", -1)])
```
- Otimiza queries que filtram por ambos os campos
- 1 = ascendente, -1 = descendente

#### 3. Índice de Texto
```python
collection.create_index([("Title", "text")])
```
- Habilita busca full-text no título
- Permite queries de texto mais rápidas

#### 4. Índice Sparse
```python
collection.create_index("Metascore", sparse=True)
```
- Índice apenas para documentos que possuem o campo
- Economiza espaço se campo é opcional

## Resultados esperados

### Exemplo de Query por Gênero
```
Drama: 234 filmes
Top 3:
  1. The Shawshank Redemption (1994) - 9.3
  2. The Godfather (1972) - 9.2
  3. The Dark Knight (2008) - 9.0
```

### Exemplo de Agregação por Certificado
```
R: média 7.95 (345 filmes)
PG-13: média 7.88 (289 filmes)
Approved: média 8.12 (145 filmes)
```

### Exemplo de Distribuição de Notas
```
0-5: 0 filmes
5-6: 5 filmes
6-7: 45 filmes
7-8: 213 filmes
8-9: 456 filmes
9-10: 281 filmes
```

## Arquivos gerados

### 1. mongodb_operations_log.txt
Registro detalhado de todas as operações:
- Conexão
- Inserção de dados
- Queries executadas
- Agregações realizadas
- Índices criados
- Erros (se houver)

### 2. advanced_queries_results.txt
Resultados das consultas avançadas:
- Queries complexas
- Agregações avançadas
- Estatísticas de índices
- Dados de performance

## Dicas de otimização

1. **Para queries frequentes:** Crie índices nos campos consultados
2. **Para agregações:** Use $match cedo para filtrar documentos
3. **Para buscas de texto:** Use índice de texto em campos descritivos
4. **Para campos opcionais:** Use índices sparse para economizar espaço
5. **Para múltiplos filtros:** Considere índices compostos

## Estrutura do documento (IMDB)

```json
{
  "Title": "1. The Shawshank Redemption (1994)",
  "Certificate": "R",
  "Duration": "142 min",
  "Genre": "Drama",
  "Rate": 9.3,
  "Metascore": 80,
  "Description": "Two imprisoned men bond...",
  "Cast": "Director: Frank Darabont | Stars: Tim Robbins...",
  "Info": "Votes: 2,295,987 | Gross: $28.34M"
}
```

## Troubleshooting

### Erro: "bad auth"
- Verifique username e password
- Verifique se IP 149.78.206.47 está autorizado

### Erro: "Connection timeout"
- Verifique internet
- Verifique se cluster URI está correto

### Erro: "FileNotFoundError"
- Certifique-se que "IMDB top 1000.csv" está no mesmo diretório

## Próximos passos

1. Modificar scripts para sua base de dados específica
2. Ajustar credenciais conforme necessário
3. Adicionar mais operações customizadas
4. Integrar com aplicação Django/Flask
5. Implementar interface web

## Referências

- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Aggregation Pipeline](https://docs.mongodb.com/manual/reference/operator/aggregation/)
- [MongoDB Indexing](https://docs.mongodb.com/manual/indexes/)
