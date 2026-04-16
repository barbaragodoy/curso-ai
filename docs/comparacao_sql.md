# Comparação MongoDB vs PostgreSQL — Etapa 6

## Estrutura de armazenamento

### MongoDB (modelo documental)
```
producoes_com_participantes
{
  "titulo": "...",
  "tipo": "Livro",
  "ano": 2018,
  "participantes": [
    { "nome": "João Silva", "papel": "Autor" },
    { "nome": "Maria Lima", "papel": "Editor" }
  ],
  "_total_participantes": 2
}
```
Cada produção carrega seus participantes diretamente. **Sem tabelas intermediárias.**

### PostgreSQL (modelo relacional)
```sql
-- 3 tabelas normalizadas
producao (id, raw_id, tipo, titulo, ano, raw_data)
pessoa   (id, raw_id, nome, raw_data)
equipe   (id, producao_raw_id, pessoa_raw_id, papel, raw_data)
```
Os dados são distribuídos em tabelas separadas e unidos por chaves estrangeiras.

---

## Comparação de consultas

### "Quais pessoas participaram desta produção?"

**MongoDB (1 consulta, sem JOIN):**
```javascript
db.producoes_com_participantes.findOne({ id_producao: "123" })
// retorna a produção COM os participantes aninhados
```

**PostgreSQL (JOIN entre 3 tabelas):**
```sql
SELECT p.nome, e.papel
FROM producao pr
JOIN equipe e ON e.producao_raw_id = pr.raw_id
JOIN pessoa p ON p.raw_id = e.pessoa_raw_id
WHERE pr.raw_id = '123';
```

### "Top 10 pessoas com mais participações"

**MongoDB:**
```javascript
db.producoes_com_participantes.aggregate([
  { $unwind: "$participantes" },
  { $group: { _id: "$participantes.nome", total: { $sum: 1 } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
])
```

**PostgreSQL:**
```sql
SELECT p.nome, COUNT(e.id) AS total
FROM pessoa p
JOIN equipe e ON e.pessoa_raw_id = p.raw_id
GROUP BY p.nome
ORDER BY total DESC
LIMIT 10;
```

---

## O que foi mais fácil no MongoDB

- Consultas de leitura que precisam de dados de múltiplas entidades (produção + pessoas) — **sem JOIN**
- Flexibilidade de schema: campos diferentes por documento não causam erro
- Inserção de lotes com estruturas heterogêneas (JSONL com campos variáveis)
- Agregações com `$unwind` em arrays aninhados são expressivas e diretas

## O que foi mais fácil no PostgreSQL

- Consultas com filtros complexos e múltiplos critérios numéricos (WHERE + AND + BETWEEN)
- Garantia de integridade referencial (chaves estrangeiras)
- Atualizações pontuais em um campo de muitas linhas (UPDATE simples vs. update em array aninhado)
- Familiaridade: SQL é mais conhecido e há mais ferramentas de visualização

## Conclusão

Para este dataset — onde a consulta dominante é "uma produção com todos os seus participantes" — o **MongoDB com modelo documental** é a escolha mais adequada. A coleção `producoes_com_participantes` permite respostas em uma única operação de leitura.

O PostgreSQL seria preferível se a aplicação precisasse frequentemente **alterar papéis de pessoas** em muitas produções de uma vez, ou se houvesse requisitos rígidos de integridade transacional.
