# Problemas Encontrados na Base BD_Producao_Artistica

## 1. Formato dos arquivos
Os dados estão em JSONL (JSON Lines) — um objeto JSON por linha. Isso difere do CSV convencional e exigiu um parser específico no extractor.

## 2. Relação entre os 3 arquivos
A base é composta por 3 arquivos com relacionamentos implícitos:

| Arquivo | Conteúdo | Relação |
|---|---|---|
| `produção.jsonl` | Dados das produções (título, tipo, ano…) | — |
| `pessoa.jsonl` | Cadastro de pessoas | — |
| `equipe.jsonl` | Relaciona pessoas a produções, com papel | `id_producao` → produção / `id_pessoa` → pessoa |

## 3. Problemas identificados na qualidade dos dados

### produção.jsonl
- **Anos inválidos:** registros com `ano` fora do intervalo 1900–2030 (valores zerados ou nulos)
- **Tipo inconsistente:** campo `tipo` com variações de capitalização e espaços extras (ex: `"livro "`, `"Livro"`, `"LIVRO"`)
- **Campos vazios:** título e descrição com valores nulos ou strings vazias

### pessoa.jsonl
- **Nomes inconsistentes:** espaços extras, variações de caixa
- **Duplicatas:** algumas pessoas aparecem mais de uma vez com IDs diferentes

### equipe.jsonl
- **IDs sem correspondência (órfãos):** registros de equipe referenciando `id_producao` ou `id_pessoa` que não existem nas demais coleções
- **Papéis nulos ou estranhos:** campo `papel` com valores `null`, string vazia, ou valores como `"N/A"`, `"?"`, `"outro"`
- **Registros duplicados:** mesma combinação (producao, pessoa, papel) aparecendo mais de uma vez

## 4. Impacto dos problemas no enriquecimento
Os IDs sem correspondência impedem que a junção entre os 3 arquivos seja completa. Registros órfãos em `equipe.jsonl` são contabilizados mas não incluídos em `producoes_com_participantes`.

---

## 5. Problemas técnicos encontrados no pipeline

### Colunas com tipos mistos no transformer
Colunas de dtype `object` no pandas podem conter valores de tipos diferentes (strings, inteiros, None). A operação `.str.strip()` aplicada diretamente sobre essas colunas falha silenciosamente — valores não-string são convertidos para `NaN`, causando perda de dados.

**Solução adotada:** substituído por `.apply(lambda x: x.strip() if isinstance(x, str) else x)`, que aplica o strip apenas em valores que são de fato strings.

### Detecção de campo nome capturando metadados ETL
A função de detecção dinâmica de campos por palavras-chave identificava `_etl_filename` como campo de nome da pessoa, pois o campo contém a substring `"name"`. Isso fazia com que participantes fossem enriquecidos com o nome do arquivo em vez do nome real da pessoa.

**Solução adotada:** campos com prefixo `_` são ignorados pela função de detecção, restringindo a busca apenas aos campos originais dos dados.

### Mismatch de IDs por tipo ou espaços no enriquecimento
O transformer pode converter IDs numéricos de string para inteiro (ex: `"1"` → `1`). Se dois arquivos tiverem o mesmo ID representado com tipos diferentes, a junção no enriquecimento falha silenciosamente — a produção não encontra sua equipe correspondente.

**Solução adotada:** todos os IDs são normalizados para `str` com `.strip()` antes do lookup, garantindo que `1` e `"1"` e `" 1"` sejam tratados como equivalentes.
