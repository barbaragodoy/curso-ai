"""
Analytics — consultas sobre as coleções MongoDB.
Cobre todos os requisitos da Etapa 5:
  - 3 consultas simples com filtro
  - 2 agregações
  - 1 ranking
  - 1 consulta mostrando vantagem do modelo escolhido

Todos os endpoints aceitam ?collection= para datasets genéricos.
Endpoints /bd/* são específicos para producoes_com_participantes.
"""
from fastapi import APIRouter, HTTPException, Query
from app.database.mongo import get_db
from app.database.postgres import run_comparison_queries, ping_postgres
from app.pipeline.loader import get_last_quality_report, list_datasets
router = APIRouter(prefix="/analytics", tags=["Analytics"])

ENRICHED = "producoes_com_participantes"


def _resolve_collection(collection: str | None) -> str:
    if collection:
        return collection
    datasets = list_datasets()
    if not datasets:
        raise HTTPException(status_code=404, detail="Nenhum dataset importado ainda.")
    return datasets[0]["collection_name"]


# ── Infraestrutura ────────────────────────────────────────

@router.get("/datasets")
def get_datasets():
    """Lista todos os datasets importados."""
    try:
        return {"datasets": list_datasets()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
def summary(collection: str | None = Query(default=None)):
    try:
        col_name = _resolve_collection(collection)
        col = get_db()[col_name]
        total = col.count_documents({})
        last = col.find_one({"_etl_timestamp": {"$exists": True}},
                            sort=[("_etl_timestamp", -1)],
                            projection={"_etl_timestamp": 1, "_id": 0})
        return {"collection": col_name, "total_records": total,
                "last_ingestion": last["_etl_timestamp"] if last else None}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quality-report")
def quality_report(collection: str | None = Query(default=None)):
    try:
        report = get_last_quality_report(collection_name=collection)
        if not report:
            return {"message": "Nenhum relatório disponível ainda."}
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Etapa 5 — Consultas simples (filtros) ─────────────────

@router.get("/bd/producoes-por-tipo")
def producoes_por_tipo():
    """[Filtro simples] Quantidade de produções agrupadas por tipo."""
    try:
        col = get_db()[ENRICHED]
        type_fields = ["tipo", "type", "tipo_producao", "modalidade", "categoria"]
        for field in type_fields:
            if col.find_one({field: {"$exists": True, "$nin": ["N/A", None]}}):
                pipeline = [
                    {"$match": {field: {"$nin": ["N/A", None, ""]}}},
                    {"$group": {"_id": f"${field}", "total": {"$sum": 1}}},
                    {"$sort": {"total": -1}},
                    {"$project": {"tipo": "$_id", "total": 1, "_id": 0}},
                ]
                return {"field": field, "data": list(col.aggregate(pipeline))}
        return {"data": [], "message": "Campo 'tipo' não encontrado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bd/producoes-por-ano")
def producoes_por_ano(ano_min: int = 1900, ano_max: int = 2030):
    """[Filtro simples] Anos com mais produções (filtra anos inválidos)."""
    try:
        col = get_db()[ENRICHED]
        year_fields = ["ano", "year", "ano_publicacao", "ano_producao"]
        for field in year_fields:
            if col.find_one({field: {"$exists": True, "$gt": ano_min}}):
                pipeline = [
                    {"$match": {field: {"$gt": ano_min, "$lte": ano_max}}},
                    {"$group": {"_id": f"${field}", "total": {"$sum": 1}}},
                    {"$sort": {"_id": 1}},
                    {"$project": {"ano": "$_id", "total": 1, "_id": 0}},
                ]
                return {"field": field, "ano_min": ano_min, "ano_max": ano_max,
                        "data": list(col.aggregate(pipeline))}
        return {"data": [], "message": "Campo 'ano' não encontrado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bd/producoes-com-muitos-participantes")
def producoes_com_muitos_participantes(minimo: int = 3):
    """[Filtro simples] Produções com pelo menos N participantes."""
    try:
        col = get_db()[ENRICHED]
        result = list(
            col.find(
                {"_total_participantes": {"$gte": minimo}},
                {"_id": 0, "_hash": 0, "participantes": 0},
            ).sort("_total_participantes", -1).limit(50)
        )
        return {"minimo_participantes": minimo, "total_encontradas": len(result), "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Etapa 5 — Agregações ──────────────────────────────────

@router.get("/bd/media-participantes-por-tipo")
def media_participantes_por_tipo():
    """[Agregação] Média de participantes por tipo de produção."""
    try:
        col = get_db()[ENRICHED]
        type_fields = ["tipo", "type", "modalidade", "categoria"]
        for field in type_fields:
            if col.find_one({field: {"$exists": True, "$nin": ["N/A", None]}}):
                pipeline = [
                    {"$match": {field: {"$nin": ["N/A", None, ""]}}},
                    {"$group": {
                        "_id": f"${field}",
                        "media_participantes": {"$avg": "$_total_participantes"},
                        "total_producoes": {"$sum": 1},
                    }},
                    {"$sort": {"media_participantes": -1}},
                    {"$project": {
                        "tipo": "$_id",
                        "media_participantes": {"$round": ["$media_participantes", 2]},
                        "total_producoes": 1,
                        "_id": 0,
                    }},
                ]
                return {"field": field, "data": list(col.aggregate(pipeline))}
        return {"data": [], "message": "Campo 'tipo' não encontrado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bd/papeis-mais-frequentes")
def papeis_mais_frequentes():
    """[Agregação] Papéis mais frequentes entre todos os participantes."""
    try:
        col = get_db()[ENRICHED]
        pipeline = [
            {"$unwind": "$participantes"},
            {"$match": {"participantes.papel": {"$nin": ["N/A", None, ""]}}},
            {"$group": {"_id": "$participantes.papel", "total": {"$sum": 1}}},
            {"$sort": {"total": -1}},
            {"$limit": 15},
            {"$project": {"papel": "$_id", "total": 1, "_id": 0}},
        ]
        return {"data": list(col.aggregate(pipeline))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Etapa 5 — Ranking ─────────────────────────────────────

@router.get("/bd/ranking-pessoas")
def ranking_pessoas(limit: int = 20):
    """[Ranking] Top pessoas com mais participações em produções."""
    try:
        col = get_db()[ENRICHED]
        pipeline = [
            {"$unwind": "$participantes"},
            {"$match": {"participantes.nome": {"$nin": ["N/A", None, ""]}}},
            {"$group": {
                "_id": "$participantes.nome",
                "total_participacoes": {"$sum": 1},
                "papeis": {"$addToSet": "$participantes.papel"},
            }},
            {"$sort": {"total_participacoes": -1}},
            {"$limit": limit},
            {"$project": {
                "nome": "$_id",
                "total_participacoes": 1,
                "papeis": 1,
                "_id": 0,
            }},
        ]
        return {"limit": limit, "data": list(col.aggregate(pipeline))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Etapa 5 — Vantagem do modelo (dados aninhados) ────────

@router.get("/bd/producao-completa/{producao_id}")
def producao_completa(producao_id: str):
    """
    [Vantagem do modelo] Retorna uma produção completa com todos os participantes
    em uma única consulta — sem JOIN. Demonstra a vantagem do modelo documental.
    """
    try:
        col = get_db()[ENRICHED]
        id_fields = ["id_producao", "id_prod", "producao_id", "id"]
        for field in id_fields:
            doc = col.find_one({field: producao_id}, {"_id": 0, "_hash": 0})
            if doc:
                return {
                    "note": (
                        "No MongoDB, produção + participantes retorna em 1 consulta. "
                        "No PostgreSQL, isso exigiria JOIN entre 3 tabelas."
                    ),
                    "data": doc,
                }
        return {"message": f"Produção '{producao_id}' não encontrada.", "data": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Etapa 6 — Comparação PostgreSQL ──────────────────────

@router.get("/comparacao-sql")
def comparacao_sql():
    """
    [Etapa 6] Executa consultas de comparação no PostgreSQL e retorna resultados
    lado a lado com a abordagem MongoDB.
    """
    if not ping_postgres():
        raise HTTPException(
            status_code=503,
            detail="PostgreSQL não disponível. Verifique se o container está rodando e a pipeline foi executada."
        )
    try:
        pg_results = run_comparison_queries()
        return {
            "mongodb_approach": "Dados aninhados em producoes_com_participantes — consultas sem JOIN",
            "postgresql_approach": "Tabelas normalizadas — consultas requerem JOIN entre producao, pessoa e equipe",
            "postgresql_results": pg_results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Dashboard genérico (datasets CSV/URL) ────────────────

@router.get("/by-year")
def by_year(collection: str | None = Query(default=None)):
    try:
        col_name = _resolve_collection(collection)
        col = get_db()[col_name]
        for field in ["ano", "year", "ano_publicacao", "data"]:
            if col.find_one({field: {"$exists": True, "$nin": ["N/A", None, 0]}}):
                pipeline = [
                    {"$match": {field: {"$nin": ["N/A", None, 0]}}},
                    {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
                    {"$sort": {"_id": 1}},
                    {"$project": {"year": "$_id", "count": 1, "_id": 0}},
                ]
                result = list(col.aggregate(pipeline))
                if result:
                    return {"field_used": field, "data": result}
        return {"field_used": None, "data": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-type")
def by_type(collection: str | None = Query(default=None)):
    try:
        col_name = _resolve_collection(collection)
        col = get_db()[col_name]
        for field in ["tipo", "type", "categoria", "modalidade"]:
            if col.find_one({field: {"$exists": True, "$nin": ["N/A", None]}}):
                pipeline = [
                    {"$match": {field: {"$nin": ["N/A", None]}}},
                    {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$project": {"type": "$_id", "count": 1, "_id": 0}},
                ]
                result = list(col.aggregate(pipeline))
                if result:
                    return {"field_used": field, "data": result}
        return {"field_used": None, "data": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-author")
def by_author(collection: str | None = Query(default=None)):
    try:
        col_name = _resolve_collection(collection)
        col = get_db()[col_name]
        for field in ["autor", "author", "nome_autor", "responsavel", "artista", "nome"]:
            if col.find_one({field: {"$exists": True, "$nin": ["N/A", None]}}):
                pipeline = [
                    {"$match": {field: {"$nin": ["N/A", None]}}},
                    {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
                    {"$sort": {"count": -1}},
                    {"$limit": 20},
                    {"$project": {"author": "$_id", "count": 1, "_id": 0}},
                ]
                result = list(col.aggregate(pipeline))
                if result:
                    return {"field_used": field, "data": result}
        return {"field_used": None, "data": []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
