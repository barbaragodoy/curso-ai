# Decisões Técnicas do Projeto

## 1. Modelo documental: `producoes_com_participantes`

**Decisão:** Usar documentos ricos com participantes aninhados em vez de coleções separadas normalizadas.

**Justificativa:**  
O MongoDB é projetado para o modelo documental. Aninhar os participantes em cada produção elimina a necessidade de JOINs para as consultas mais comuns (ex: "quais pessoas participaram desta produção?"). O custo é a redundância de dados de pessoa em múltiplos documentos, o que é aceitável dado o volume da base.

**Alternativa considerada:** Manter `producao_clean`, `pessoa_clean`, `equipe_clean` separadas e usar `$lookup` para unir. Descartada porque derrota o propósito de usar um banco documental.

## 2. Duas camadas de armazenamento: RAW e CLEAN

**Decisão:** Guardar o dado bruto em coleções `raw_*` antes de qualquer tratamento.

**Justificativa:**  
Permite reprocessar os dados no futuro com novas regras de tratamento sem precisar reimportar os arquivos originais. Também serve como auditoria: é possível comparar o dado original com o tratado a qualquer momento.

## 3. Upsert com hash SHA-256 nas coleções CLEAN

**Decisão:** Usar hash do conteúdo do registro como chave de upsert.

**Justificativa:**  
Torna a pipeline idempotente — pode ser executada múltiplas vezes com o mesmo arquivo sem duplicar dados. Registros alterados são atualizados; novos são inseridos; registros idênticos são ignorados.

## 4. Detecção dinâmica de campos

**Decisão:** Em vez de hardcodar nomes de campos (ex: `producao["id_producao"]`), o sistema detecta automaticamente os campos baseado em palavras-chave.

**Justificativa:**  
A base pode ter variações de nomenclatura entre versões. A detecção dinâmica torna o pipeline mais resiliente.

## 5. PostgreSQL apenas para comparação

**Decisão:** O PostgreSQL recebe os dados tratados mas não é o banco principal da aplicação.

**Justificativa:**  
O trabalho foca no banco não relacional. O PostgreSQL serve exclusivamente para demonstrar as diferenças de modelo e consultas na Etapa 6, conforme exigido pelo professor.

## 6. Docker Compose com 4 serviços

**Decisão:** Backend (FastAPI) + MongoDB + PostgreSQL + Frontend (Nginx) em docker-compose.

**Justificativa:**
Permite que qualquer membro do grupo rode o projeto completo com um único `docker compose up --build`, sem instalar nada localmente além do Docker.

## 7. Exclusão de campos `_etl_*` na detecção dinâmica de campos

**Decisão:** A função `_find_id_field` ignora qualquer campo cujo nome comece com `_` ao buscar campos de ID e nome.

**Justificativa:**
Durante o enriquecimento, a detecção dinâmica de campos por palavras-chave (`"nome"`, `"name"`, `"id"`, etc.) estava capturando campos de metadados ETL indevidamente. Por exemplo, `_etl_filename` contém a substring `"name"` e era incorretamente identificado como o campo de nome da pessoa. Ao excluir campos com prefixo `_`, garante-se que apenas campos reais dos dados originais são considerados.

## 8. Normalização de IDs para string no enriquecimento

**Decisão:** Todos os IDs usados como chave de lookup no enriquecimento são convertidos para `str` com `.strip()` antes da comparação.

**Justificativa:**
Após o transformer, campos numéricos como `id_producao` podem ser armazenados como inteiros (`1`) ou strings (`"1"`) dependendo do arquivo de origem. Sem normalização, a junção entre os 3 datasets falharia silenciosamente quando os tipos diferissem. O `.strip()` adicional resolve casos de espaços acidentais nos valores.
