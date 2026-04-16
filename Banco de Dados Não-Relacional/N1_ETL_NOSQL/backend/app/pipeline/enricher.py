"""
Enricher — constrói a coleção `producoes_com_participantes` no MongoDB.

Junta os 3 datasets tratados:
  producao_clean  →  equipe_clean (por producao_id)  →  pessoa_clean (por pessoa_id)

Resultado: cada documento de produção traz sua lista de participantes aninhada.

Exemplo de documento gerado:
{
  "_id": "...",
  "titulo": "Nome da Obra",
  "tipo": "Livro",
  "ano": 2018,
  ...demais campos da produção...
  "participantes": [
    { "nome": "João Silva", "papel": "Autor", "pessoa_id": "123" },
    { "nome": "Maria Lima", "papel": "Editor", "pessoa_id": "456" }
  ],
  "_total_participantes": 2,
  "_enriched_at": "2024-..."
}
"""
from __future__ import annotations

from datetime import datetime
from typing import Any

from app.database.mongo import get_db


ENRICHED_COLLECTION = "producoes_com_participantes"


def _find_id_field(sample: dict, keywords: list[str]) -> str | None:
    """Encontra o campo de ID em um documento baseado em palavras-chave.
    Ignora campos de metadados ETL (prefixo _etl ou _).
    """
    for key in sample.keys():
        if key.startswith("_"):
            continue
        lower = key.lower()
        if any(kw in lower for kw in keywords):
            return key
    return None


def build_producoes_com_participantes() -> dict:
    """
    Lê as coleções clean e monta `producoes_com_participantes`.
    Retorna um relatório com totais e estatísticas.
    """
    db = get_db()

    # Verificar se as coleções existem e têm dados
    producao_col = db["producao_clean"]
    equipe_col   = db["equipe_clean"]
    pessoa_col   = db["pessoa_clean"]

    total_producao = producao_col.count_documents({})
    total_equipe   = equipe_col.count_documents({})
    total_pessoa   = pessoa_col.count_documents({})

    if total_producao == 0:
        return {"error": "Coleção producao_clean está vazia. Execute a pipeline de ingestão primeiro."}

    # Descobrir nomes dos campos de ID dinamicamente
    sample_prod  = producao_col.find_one({}, {"_id": 0, "_hash": 0}) or {}
    sample_eq    = equipe_col.find_one({}, {"_id": 0, "_hash": 0}) or {}
    sample_pessoa = pessoa_col.find_one({}, {"_id": 0, "_hash": 0}) or {}

    prod_id_field   = _find_id_field(sample_prod,   ["id_producao", "id_prod", "producao_id", "id"])
    eq_prod_field   = _find_id_field(sample_eq,     ["id_producao", "producao_id", "prod_id"])
    eq_pessoa_field = _find_id_field(sample_eq,     ["id_pessoa", "pessoa_id", "id_par"])
    pessoa_id_field = _find_id_field(sample_pessoa, ["id_pessoa", "id_par", "pessoa_id", "id"])
    pessoa_name_field = _find_id_field(sample_pessoa, ["nome", "name"])
    eq_papel_field  = _find_id_field(sample_eq,     ["papel", "role", "funcao"])

    # Montar índice de pessoas por ID para lookup O(1)
    # str().strip() normaliza tipos diferentes (int vs str) e espaços acidentais
    pessoas_index: dict[Any, dict] = {}
    if pessoa_id_field:
        for p in pessoa_col.find({}, {"_id": 0, "_hash": 0}):
            key = p.get(pessoa_id_field)
            if key is not None:
                pessoas_index[str(key).strip()] = p

    # Montar índice de equipe agrupado por producao_id
    equipe_index: dict[str, list[dict]] = {}
    orphan_equipe = 0
    if eq_prod_field:
        for e in equipe_col.find({}, {"_id": 0, "_hash": 0}):
            prod_key = str(e.get(eq_prod_field, "")).strip()
            if not prod_key or prod_key == "N/A":
                orphan_equipe += 1
                continue
            equipe_index.setdefault(prod_key, []).append(e)

    # Construir documentos enriquecidos
    enriched_docs = []
    producoes_sem_equipe = 0

    for prod in producao_col.find({}, {"_id": 0, "_hash": 0}):
        prod_key = str(prod.get(prod_id_field, "")).strip() if prod_id_field else ""
        equipe_entries = equipe_index.get(prod_key, [])

        participantes = []
        for entry in equipe_entries:
            pessoa_key = str(entry.get(eq_pessoa_field, "")).strip() if eq_pessoa_field else ""
            pessoa_data = pessoas_index.get(pessoa_key, {})

            participante = {
                "papel": entry.get(eq_papel_field, "N/A") if eq_papel_field else "N/A",
            }
            if pessoa_data:
                participante["nome"] = pessoa_data.get(pessoa_name_field, "N/A") if pessoa_name_field else "N/A"
                participante["pessoa_id"] = pessoa_key
                # Inclui demais campos da pessoa (exceto id e metadados)
                for k, v in pessoa_data.items():
                    if k not in (pessoa_id_field, pessoa_name_field) and not k.startswith("_"):
                        participante[k] = v
            else:
                participante["nome"] = "N/A"
                participante["pessoa_id"] = pessoa_key

            participantes.append(participante)

        if not participantes:
            producoes_sem_equipe += 1

        doc = {
            **prod,
            "participantes": participantes,
            "_total_participantes": len(participantes),
            "_enriched_at": datetime.utcnow().isoformat(),
        }
        enriched_docs.append(doc)

    # Salvar na coleção enriquecida (recria do zero)
    enriched_col = db[ENRICHED_COLLECTION]
    enriched_col.drop()

    inserted = 0
    BATCH_SIZE = 500
    if enriched_docs:
        for i in range(0, len(enriched_docs), BATCH_SIZE):
            batch = enriched_docs[i : i + BATCH_SIZE]
            result = enriched_col.insert_many(batch, ordered=False)
            inserted += len(result.inserted_ids)

    # Índices úteis para as consultas analíticas
    enriched_col.create_index("_total_participantes")
    if prod_id_field:
        enriched_col.create_index(prod_id_field)

    return {
        "collection": ENRICHED_COLLECTION,
        "total_producoes": total_producao,
        "total_equipe_registros": total_equipe,
        "total_pessoas": total_pessoa,
        "producoes_enriquecidas": inserted,
        "producoes_sem_equipe": producoes_sem_equipe,
        "orphan_equipe_records": orphan_equipe,
        "field_mapping": {
            "producao_id_field": prod_id_field,
            "equipe_producao_field": eq_prod_field,
            "equipe_pessoa_field": eq_pessoa_field,
            "pessoa_id_field": pessoa_id_field,
            "pessoa_name_field": pessoa_name_field,
            "papel_field": eq_papel_field,
        },
    }
