"""
PostgreSQL — conexão e carga simples para comparação com MongoDB (Etapa 6).
Usa psycopg2. A URI vem da variável de ambiente POSTGRES_URI.
"""
from __future__ import annotations

import os
import json
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values

POSTGRES_URI = os.getenv(
    "POSTGRES_URI",
    "postgresql://etl_user:etl_pass@postgres:5432/etl_db"
)


def get_conn():
    return psycopg2.connect(POSTGRES_URI)


def ping_postgres() -> bool:
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return True
    except Exception:
        return False


def setup_tables(conn):
    """Cria as tabelas de comparação se não existirem."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS producao (
                id SERIAL PRIMARY KEY,
                raw_id TEXT,
                tipo TEXT,
                titulo TEXT,
                ano INTEGER,
                raw_data JSONB,
                ingested_at TIMESTAMP DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS pessoa (
                id SERIAL PRIMARY KEY,
                raw_id TEXT,
                nome TEXT,
                raw_data JSONB,
                ingested_at TIMESTAMP DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS equipe (
                id SERIAL PRIMARY KEY,
                producao_raw_id TEXT,
                pessoa_raw_id TEXT,
                papel TEXT,
                raw_data JSONB,
                ingested_at TIMESTAMP DEFAULT NOW()
            );
        """)
    conn.commit()


def _find_field(record: dict, keywords: list[str]) -> str | None:
    for key in record.keys():
        if any(kw in key.lower() for kw in keywords):
            return key
    return None


def load_to_postgres(
    producao_records: list[dict],
    pessoa_records: list[dict],
    equipe_records: list[dict],
) -> dict:
    """
    Carrega os dados tratados no PostgreSQL.
    Trunca as tabelas antes de inserir (carga completa).
    """
    try:
        conn = get_conn()
        setup_tables(conn)

        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE equipe, producao, pessoa RESTART IDENTITY CASCADE;")

        # ── Produção ──
        prod_inserted = 0
        if producao_records:
            sample = producao_records[0]
            id_field    = _find_field(sample, ["id_producao", "id_prod", "producao_id", "id"])
            tipo_field  = _find_field(sample, ["tipo", "type", "modalidade"])
            titulo_field = _find_field(sample, ["titulo", "title", "nome", "descricao"])
            ano_field   = _find_field(sample, ["ano", "year", "ano_publicacao"])

            rows = []
            for r in producao_records:
                raw_id = str(r.get(id_field, "")) if id_field else ""
                tipo   = str(r.get(tipo_field, ""))[:500] if tipo_field else ""
                titulo = str(r.get(titulo_field, ""))[:1000] if titulo_field else ""
                try:
                    ano = int(r.get(ano_field, 0)) if ano_field else 0
                except (ValueError, TypeError):
                    ano = 0
                clean = {k: v for k, v in r.items() if not k.startswith("_")}
                rows.append((raw_id, tipo, titulo, ano, json.dumps(clean, default=str)))

            with conn.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO producao (raw_id, tipo, titulo, ano, raw_data) VALUES %s",
                    rows,
                )
            conn.commit()
            prod_inserted = len(rows)

        # ── Pessoa ──
        pessoa_inserted = 0
        if pessoa_records:
            sample = pessoa_records[0]
            id_field   = _find_field(sample, ["id_pessoa", "id_par", "pessoa_id", "id"])
            nome_field = _find_field(sample, ["nome", "name"])

            rows = []
            for r in pessoa_records:
                raw_id = str(r.get(id_field, "")) if id_field else ""
                nome   = str(r.get(nome_field, ""))[:500] if nome_field else ""
                clean  = {k: v for k, v in r.items() if not k.startswith("_")}
                rows.append((raw_id, nome, json.dumps(clean, default=str)))

            with conn.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO pessoa (raw_id, nome, raw_data) VALUES %s",
                    rows,
                )
            conn.commit()
            pessoa_inserted = len(rows)

        # ── Equipe ──
        equipe_inserted = 0
        if equipe_records:
            sample = equipe_records[0]
            prod_id_field   = _find_field(sample, ["id_producao", "producao_id", "prod_id"])
            pessoa_id_field = _find_field(sample, ["id_pessoa", "pessoa_id", "id_par"])
            papel_field     = _find_field(sample, ["papel", "role", "funcao"])

            rows = []
            for r in equipe_records:
                prod_id  = str(r.get(prod_id_field, "")) if prod_id_field else ""
                pess_id  = str(r.get(pessoa_id_field, "")) if pessoa_id_field else ""
                papel    = str(r.get(papel_field, ""))[:200] if papel_field else ""
                clean    = {k: v for k, v in r.items() if not k.startswith("_")}
                rows.append((prod_id, pess_id, papel, json.dumps(clean, default=str)))

            with conn.cursor() as cur:
                execute_values(
                    cur,
                    "INSERT INTO equipe (producao_raw_id, pessoa_raw_id, papel, raw_data) VALUES %s",
                    rows,
                )
            conn.commit()
            equipe_inserted = len(rows)

        conn.close()

        return {
            "status": "success",
            "producao_inserted": prod_inserted,
            "pessoa_inserted": pessoa_inserted,
            "equipe_inserted": equipe_inserted,
        }

    except Exception as e:
        return {"status": "error", "detail": str(e)}


def run_comparison_queries() -> dict:
    """
    Executa consultas de comparação no PostgreSQL para a Etapa 6.
    Retorna os resultados com os SQLs usados.
    """
    results = {}
    try:
        conn = get_conn()
        with conn.cursor() as cur:

            # Consulta 1: produções por tipo
            cur.execute("""
                SELECT tipo, COUNT(*) AS total
                FROM producao
                WHERE tipo IS NOT NULL AND tipo != ''
                GROUP BY tipo
                ORDER BY total DESC
                LIMIT 15;
            """)
            results["producoes_por_tipo"] = {
                "sql": "SELECT tipo, COUNT(*) FROM producao GROUP BY tipo ORDER BY total DESC",
                "data": [{"tipo": r[0], "total": r[1]} for r in cur.fetchall()],
            }

            # Consulta 2: anos com mais produções
            cur.execute("""
                SELECT ano, COUNT(*) AS total
                FROM producao
                WHERE ano > 1900 AND ano <= 2030
                GROUP BY ano
                ORDER BY total DESC
                LIMIT 10;
            """)
            results["anos_com_mais_producoes"] = {
                "sql": "SELECT ano, COUNT(*) FROM producao WHERE ano > 1900 GROUP BY ano ORDER BY total DESC",
                "data": [{"ano": r[0], "total": r[1]} for r in cur.fetchall()],
            }

            # Consulta 3: top pessoas com mais participações (JOIN)
            cur.execute("""
                SELECT p.nome, COUNT(e.id) AS participacoes
                FROM pessoa p
                JOIN equipe e ON e.pessoa_raw_id = p.raw_id
                GROUP BY p.nome
                ORDER BY participacoes DESC
                LIMIT 10;
            """)
            results["top_pessoas"] = {
                "sql": "SELECT p.nome, COUNT(*) FROM pessoa p JOIN equipe e ON e.pessoa_raw_id = p.raw_id GROUP BY p.nome ORDER BY participacoes DESC",
                "data": [{"nome": r[0], "participacoes": r[1]} for r in cur.fetchall()],
            }

            # Consulta 4: papéis mais frequentes
            cur.execute("""
                SELECT papel, COUNT(*) AS total
                FROM equipe
                WHERE papel IS NOT NULL AND papel != ''
                GROUP BY papel
                ORDER BY total DESC
                LIMIT 10;
            """)
            results["papeis_mais_frequentes"] = {
                "sql": "SELECT papel, COUNT(*) FROM equipe GROUP BY papel ORDER BY total DESC",
                "data": [{"papel": r[0], "total": r[1]} for r in cur.fetchall()],
            }

        conn.close()
        results["note"] = (
            "PostgreSQL requer JOIN explícito entre tabelas. "
            "No MongoDB, os participantes já estão aninhados em cada produção, "
            "eliminando a necessidade de JOIN para consultas de leitura."
        )
    except Exception as e:
        results["error"] = str(e)

    return results
