"""
Loader — carga no MongoDB com duas camadas:
  - RAW: dado como veio (sem tratamento), coleções raw_*
  - CLEAN: dado tratado, coleções *_clean
Também mantém índice de datasets e relatórios de qualidade.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime

import pandas as pd
from pymongo import UpdateOne, InsertOne
from pymongo.errors import BulkWriteError

from app.database.mongo import get_db
from app.config import QUALITY_COLLECTION, DATASETS_COLLECTION


# ── Utilitários ────────────────────────────────────────────

def _slugify(name: str) -> str:
    name = re.sub(r"\.[a-zA-Z0-9]+$", "", name)
    name = name.rstrip("/").split("/")[-1].split("?")[0]
    nfkd = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in nfkd if not unicodedata.combining(c))
    name = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return name[:80] if name else "dataset"


def _record_hash(record: dict) -> str:
    clean = {k: v for k, v in record.items()
             if not k.startswith("_etl") and k not in ("_hash", "_id")}
    return hashlib.sha256(
        json.dumps(clean, sort_keys=True, default=str).encode()
    ).hexdigest()


# ── Carga RAW (dado como veio) ────────────────────────────

def save_raw(records: list[dict], collection_name: str) -> dict:
    """
    Salva registros brutos no MongoDB sem nenhum tratamento.
    Usado na Etapa 2 do trabalho (raw_producao, raw_pessoa, raw_equipe).
    Não usa upsert — insere tudo para preservar o dado original.
    """
    db = get_db()
    col = db[collection_name]

    # Adiciona apenas timestamp de ingestão, sem alterar o dado
    now = datetime.utcnow().isoformat()
    docs = [{**r, "_raw_ingested_at": now} for r in records]

    if not docs:
        return {"collection": collection_name, "inserted": 0}

    try:
        result = col.insert_many(docs, ordered=False)
        inserted = len(result.inserted_ids)
    except Exception as e:
        inserted = 0

    return {"collection": collection_name, "inserted": inserted}


# ── Carga CLEAN (dado tratado, com upsert) ────────────────

def load(df: pd.DataFrame, source_name: str, collection_name: str | None = None) -> dict:
    """
    Insere/atualiza registros tratados no MongoDB.
    Se collection_name não for passado, deriva do source_name.
    """
    db = get_db()
    col_name = collection_name or _slugify(source_name)
    col = db[col_name]
    col.create_index("_hash", unique=True, background=True)

    records = df.to_dict(orient="records")
    operations = []

    for rec in records:
        rec_hash = _record_hash(rec)
        rec["_hash"] = rec_hash
        operations.append(
            UpdateOne(
                {"_hash": rec_hash},
                {
                    "$set": rec,
                    "$setOnInsert": {"_created_at": datetime.utcnow().isoformat()},
                },
                upsert=True,
            )
        )

    inserted = updated = errors = 0
    BATCH_SIZE = 500

    for i in range(0, len(operations), BATCH_SIZE):
        batch = operations[i : i + BATCH_SIZE]
        try:
            result = col.bulk_write(batch, ordered=False)
            inserted += result.upserted_count
            updated += result.modified_count
        except BulkWriteError as bwe:
            errors += len(bwe.details.get("writeErrors", []))
            inserted += bwe.details.get("nUpserted", 0)
            updated += bwe.details.get("nModified", 0)

    _register_dataset(col_name, source_name, len(records), inserted, updated)

    return {
        "collection_name": col_name,
        "total_processed": len(records),
        "inserted": inserted,
        "updated": updated,
        "skipped": len(records) - inserted - updated - errors,
        "errors": errors,
    }


def _register_dataset(collection_name, source_name, total, inserted, updated):
    db = get_db()
    db[DATASETS_COLLECTION].update_one(
        {"collection_name": collection_name},
        {
            "$set": {
                "collection_name": collection_name,
                "source_name": source_name,
                "last_ingestion": datetime.utcnow().isoformat(),
                "last_inserted": inserted,
                "last_updated": updated,
            },
            "$inc": {"total_ingestions": 1},
            "$setOnInsert": {"first_ingestion": datetime.utcnow().isoformat()},
        },
        upsert=True,
    )


# ── Relatórios de Qualidade ───────────────────────────────

def save_quality_report(report: dict) -> str:
    db = get_db()
    result = db[QUALITY_COLLECTION].insert_one(report)
    return str(result.inserted_id)


def get_last_quality_report(collection_name: str | None = None) -> dict | None:
    db = get_db()
    query = {}
    if collection_name:
        query["source"] = {"$regex": collection_name}
    return db[QUALITY_COLLECTION].find_one(
        query, sort=[("generated_at", -1)], projection={"_id": 0}
    )


def list_datasets() -> list[dict]:
    db = get_db()
    return list(db[DATASETS_COLLECTION].find({}, {"_id": 0}).sort("last_ingestion", -1))
