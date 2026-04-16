"""
Quality Report — analisa um DataFrame e retorna um relatório detalhado
de problemas de qualidade de dados.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from datetime import datetime


def _detect_outliers_iqr(series: pd.Series) -> dict:
    """Detecta outliers usando método IQR."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    outliers = series[(series < lower) | (series > upper)]
    return {
        "count": int(outliers.count()),
        "lower_bound": round(float(lower), 4),
        "upper_bound": round(float(upper), 4),
        "min_value": round(float(series.min()), 4),
        "max_value": round(float(series.max()), 4),
    }


def generate_quality_report(df: pd.DataFrame, source: str = "unknown") -> dict:
    """
    Gera um relatório completo de qualidade de dados.

    Returns:
        dict com: total_records, duplicate_rows, columns, summary, generated_at
    """
    total = len(df)
    duplicates = int(df.duplicated().sum())

    columns_report = {}
    for col in df.columns:
        series = df[col]
        null_count = int(series.isna().sum())
        null_pct = round(null_count / total * 100, 2) if total > 0 else 0.0
        unique_count = int(series.nunique(dropna=True))
        dtype = str(series.dtype)

        col_info: dict = {
            "dtype": dtype,
            "null_count": null_count,
            "null_percentage": null_pct,
            "unique_values": unique_count,
        }

        # Para colunas categóricas/object com poucos valores únicos, lista os valores
        if series.dtype == object and unique_count <= 50:
            col_info["sample_values"] = series.dropna().unique().tolist()[:20]

        # Para colunas numéricas, detecta outliers
        if pd.api.types.is_numeric_dtype(series) and series.dropna().shape[0] > 0:
            col_info["outliers"] = _detect_outliers_iqr(series.dropna())
            col_info["mean"] = round(float(series.mean()), 4)
            col_info["std"] = round(float(series.std()), 4)

        columns_report[col] = col_info

    # Colunas com mais de 50% de nulos
    high_null_cols = [
        col for col, info in columns_report.items() if info["null_percentage"] > 50
    ]

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "source": source,
        "total_records": total,
        "total_columns": len(df.columns),
        "duplicate_rows": duplicates,
        "duplicate_percentage": round(duplicates / total * 100, 2) if total > 0 else 0.0,
        "high_null_columns": high_null_cols,
        "columns": columns_report,
        "summary": {
            "has_duplicates": duplicates > 0,
            "has_high_null_columns": len(high_null_cols) > 0,
            "overall_completeness_pct": round(
                100 - (sum(v["null_count"] for v in columns_report.values()) / (total * len(df.columns)) * 100), 2
            ) if total > 0 and len(df.columns) > 0 else 100.0,
        },
    }
