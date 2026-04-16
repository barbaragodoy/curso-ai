"""
Rota POST /pipeline/bd-producao-artistica

Pipeline completa para ingestão dos 3 arquivos JSONL do dataset do trabalho.
Recebe os 3 arquivos JSONL (produção, pessoa, equipe) e executa:

  1. Extração dos JSONL
  2. Relatório de qualidade (pré-tratamento)
  3. Carga RAW no MongoDB → raw_producao, raw_pessoa, raw_equipe
  4. Transformação (limpeza, tipagem, deduplicação)
  5. Carga CLEAN no MongoDB → producao_clean, pessoa_clean, equipe_clean
  6. Enriquecimento → producoes_com_participantes
  7. Espelhamento no PostgreSQL (Etapa 6 — comparação)
"""
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional

logger = logging.getLogger(__name__)

from app.pipeline.extractor import extract_from_jsonl
from app.pipeline.quality import generate_quality_report
from app.pipeline.transformer import transform
from app.pipeline.loader import save_raw, load, save_quality_report
from app.pipeline.enricher import build_producoes_com_participantes
from app.database.postgres import load_to_postgres, ping_postgres

router = APIRouter(prefix="/pipeline", tags=["Pipeline Principal"])
_executor = ThreadPoolExecutor(max_workers=2)


@router.post("/bd-producao-artistica")
async def pipeline_bd(
    producao: UploadFile = File(..., description="Arquivo producao.jsonl (ou produção.jsonl)"),
    pessoa:   UploadFile = File(..., description="Arquivo pessoa.jsonl"),
    equipe:   UploadFile = File(..., description="Arquivo equipe.jsonl"),
):
    """
    Pipeline completa para os 3 arquivos JSONL do dataset do trabalho.

    Recebe os 3 arquivos JSONL baixados do HuggingFace e executa todas as etapas:
    RAW → CLEAN → ENRIQUECIMENTO → PostgreSQL.
    """
    try:
        prod_bytes   = await producao.read()
        pessoa_bytes = await pessoa.read()
        equipe_bytes = await equipe.read()

        prod_filename   = producao.filename
        pessoa_filename = pessoa.filename
        equipe_filename = equipe.filename
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler arquivos: {e}")

    def _run_pipeline():
        results = {}

        # ── 1. Extração ───────────────────────────────────
        df_prod   = extract_from_jsonl(prod_bytes,   filename=prod_filename)
        df_pessoa = extract_from_jsonl(pessoa_bytes, filename=pessoa_filename)
        df_equipe = extract_from_jsonl(equipe_bytes, filename=equipe_filename)

        results["extract"] = {
            "producao_rows": len(df_prod),
            "pessoa_rows":   len(df_pessoa),
            "equipe_rows":   len(df_equipe),
        }

        # ── 2. Relatório de Qualidade (pré-tratamento) ────
        qr_prod   = generate_quality_report(df_prod,   source="jsonl:producao")
        qr_pessoa = generate_quality_report(df_pessoa, source="jsonl:pessoa")
        qr_equipe = generate_quality_report(df_equipe, source="jsonl:equipe")

        save_quality_report(qr_prod)
        save_quality_report(qr_pessoa)
        save_quality_report(qr_equipe)

        results["quality"] = {
            "producao": {
                "total_records": qr_prod["total_records"],
                "duplicate_rows": qr_prod["duplicate_rows"],
                "completeness_pct": qr_prod["summary"]["overall_completeness_pct"],
                "high_null_columns": qr_prod["high_null_columns"],
            },
            "pessoa": {
                "total_records": qr_pessoa["total_records"],
                "duplicate_rows": qr_pessoa["duplicate_rows"],
                "completeness_pct": qr_pessoa["summary"]["overall_completeness_pct"],
                "high_null_columns": qr_pessoa["high_null_columns"],
            },
            "equipe": {
                "total_records": qr_equipe["total_records"],
                "duplicate_rows": qr_equipe["duplicate_rows"],
                "completeness_pct": qr_equipe["summary"]["overall_completeness_pct"],
                "high_null_columns": qr_equipe["high_null_columns"],
            },
        }

        # ── 3. Carga RAW (dado como veio) ─────────────────
        raw_prod   = save_raw(df_prod.to_dict("records"),   "raw_producao")
        raw_pessoa = save_raw(df_pessoa.to_dict("records"), "raw_pessoa")
        raw_equipe = save_raw(df_equipe.to_dict("records"), "raw_equipe")

        results["raw_load"] = {
            "raw_producao": raw_prod,
            "raw_pessoa":   raw_pessoa,
            "raw_equipe":   raw_equipe,
        }

        # ── 4 & 5. Transformação + Carga CLEAN ────────────
        df_prod_clean   = transform(df_prod,   source="jsonl", source_name="producao.jsonl")
        df_pessoa_clean = transform(df_pessoa, source="jsonl", source_name="pessoa.jsonl")
        df_equipe_clean = transform(df_equipe, source="jsonl", source_name="equipe.jsonl")

        clean_prod   = load(df_prod_clean,   source_name="producao.jsonl",  collection_name="producao_clean")
        clean_pessoa = load(df_pessoa_clean, source_name="pessoa.jsonl",    collection_name="pessoa_clean")
        clean_equipe = load(df_equipe_clean, source_name="equipe.jsonl",    collection_name="equipe_clean")

        results["clean_load"] = {
            "producao_clean": clean_prod,
            "pessoa_clean":   clean_pessoa,
            "equipe_clean":   clean_equipe,
        }

        # ── 6. Enriquecimento ─────────────────────────────
        enrichment = build_producoes_com_participantes()
        results["enrichment"] = enrichment

        # ── 7. PostgreSQL (comparação) ────────────────────
        if ping_postgres():
            pg_result = load_to_postgres(
                producao_records=df_prod_clean.to_dict("records"),
                pessoa_records=df_pessoa_clean.to_dict("records"),
                equipe_records=df_equipe_clean.to_dict("records"),
            )
            results["postgresql"] = pg_result
        else:
            results["postgresql"] = {"status": "skipped", "detail": "PostgreSQL não disponível."}

        return results

    try:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(_executor, _run_pipeline)
    except Exception as e:
        logger.exception("Erro na pipeline bd-producao-artistica")
        raise HTTPException(status_code=500, detail="Erro interno na pipeline. Verifique os logs do servidor.")

    return {
        "status": "success",
        "pipeline": "etl_principal",
        "stages": results,
        "collections_created": [
            "raw_producao", "raw_pessoa", "raw_equipe",
            "producao_clean", "pessoa_clean", "equipe_clean",
            "producoes_com_participantes",
        ],
    }
