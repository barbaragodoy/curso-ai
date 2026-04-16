"""
Transformer — aplica todas as transformações de limpeza e padronização
no DataFrame antes da carga no MongoDB.
"""
from __future__ import annotations

import hashlib
import logging
import re
import unicodedata
from datetime import datetime
from typing import Literal

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


# Formatos de data que a pipeline tenta interpretar
DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y/%m/%d",
    "%d/%m/%y",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
]

# Palavras que indicam que uma coluna é provavelmente uma data
DATE_KEYWORDS = ("data", "date", "ano", "year", "dt_", "_dt", "publicacao", "criacao", "nascimento")


def _remove_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _normalize_column_name(name: str) -> str:
    """Transforma nome de coluna em snake_case sem acentos."""
    name = str(name).strip()
    name = _remove_accents(name)
    name = name.lower()
    name = re.sub(r"[^\w\s]", "", name)       # remove pontuação
    name = re.sub(r"\s+", "_", name)           # espaços -> _
    name = re.sub(r"_+", "_", name)            # múltiplos _ -> um
    name = name.strip("_")
    return name


def _try_parse_date(series: pd.Series) -> pd.Series | None:
    """Tenta converter uma série para datetime. Retorna None se falhar."""
    for fmt in DATE_FORMATS:
        try:
            converted = pd.to_datetime(series, format=fmt, errors="raise")
            return converted.dt.strftime("%Y-%m-%dT%H:%M:%S")
        except Exception:
            continue
    # Última tentativa genérica
    try:
        converted = pd.to_datetime(series, infer_datetime_format=True, errors="raise")
        return converted.dt.strftime("%Y-%m-%dT%H:%M:%S")
    except Exception:
        return None


def _is_likely_date_column(col_name: str, series: pd.Series) -> bool:
    """Heurística: nome contém keyword de data e série tem tipo object ou já é datetime."""
    lower = col_name.lower()
    has_keyword = any(kw in lower for kw in DATE_KEYWORDS)
    is_object = series.dtype == object
    return has_keyword and is_object


def transform(
    df: pd.DataFrame,
    source: Literal["csv", "url"] = "csv",
    source_name: str = "unknown",
) -> pd.DataFrame:
    """
    Aplica todas as transformações ao DataFrame.
    Retorna um novo DataFrame transformado.
    """
    df = df.copy()

    # 1. Normalizar nomes de colunas
    df.columns = [_normalize_column_name(c) for c in df.columns]

    # 2. Strip em todas as colunas de texto (usa apply para evitar crash em colunas mistas)
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # 3. Remover linhas completamente duplicadas
    df = df.drop_duplicates()

    # 4. Tentar converter colunas de data
    for col in df.columns:
        if _is_likely_date_column(col, df[col]):
            converted = _try_parse_date(df[col])
            if converted is not None:
                df[col] = converted

    # 5. Coerce colunas numéricas (object que parecem ser números)
    for col in df.select_dtypes(include="object").columns:
        sample = df[col].dropna().head(50)
        numeric_count = pd.to_numeric(sample, errors="coerce").notna().sum()
        if numeric_count / max(len(sample), 1) > 0.8:
            non_numeric = df[col].dropna()[pd.to_numeric(df[col].dropna(), errors="coerce").isna()]
            if not non_numeric.empty:
                logger.warning(
                    "Coluna '%s': %d valor(es) não numérico(s) serão convertidos para NaN → 0. "
                    "Exemplos: %s",
                    col, len(non_numeric), non_numeric.head(3).tolist(),
                )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. Preencher nulos
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("N/A")
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(0)

    # 7. Substituir infinitos por 0 em colunas numéricas
    df.replace([np.inf, -np.inf], 0, inplace=True)

    # 8. Adicionar metadados ETL
    etl_ts = datetime.utcnow().isoformat()
    df["_etl_source"] = source
    df["_etl_timestamp"] = etl_ts
    df["_etl_filename"] = source_name

    return df
