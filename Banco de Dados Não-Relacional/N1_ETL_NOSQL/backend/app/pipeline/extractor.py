"""
Extractor — suporta CSV (bytes), JSONL (bytes) e URL pública (CSV ou JSON).
URLs do Google Sheets são convertidas automaticamente para export CSV.
"""
import io
import json
import re
from typing import Literal

import httpx
import pandas as pd


def _normalize_google_sheets_url(url: str) -> str:
    pattern = r"https://docs\.google\.com/spreadsheets/d/([^/]+)"
    match = re.match(pattern, url)
    if match:
        sheet_id = match.group(1)
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    return url


def extract_from_csv(content: bytes, filename: str = "upload.csv") -> pd.DataFrame:
    """Lê conteúdo CSV em bytes e retorna um DataFrame."""
    try:
        df = pd.read_csv(io.BytesIO(content), encoding="utf-8", sep=None, engine="python")
    except UnicodeDecodeError:
        df = pd.read_csv(io.BytesIO(content), encoding="latin-1", sep=None, engine="python")
    return df


def extract_from_jsonl(content: bytes, filename: str = "upload.jsonl") -> pd.DataFrame:
    """
    Lê conteúdo JSONL (JSON Lines) em bytes e retorna um DataFrame.
    Cada linha do arquivo deve ser um objeto JSON válido.
    Suporta também arquivos JSON array normais como fallback.
    """
    text = content.decode("utf-8", errors="replace").strip()

    records = []
    errors = 0

    # Tenta linha a linha (JSONL)
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            errors += 1

    # Fallback: tenta como JSON array normal
    if not records:
        try:
            data = json.loads(text)
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                records = [data]
        except json.JSONDecodeError:
            pass

    if not records:
        raise ValueError(
            f"Não foi possível interpretar '{filename}' como JSONL ou JSON. "
            f"Linhas com erro: {errors}"
        )

    return pd.DataFrame(records)


def extract_from_url(url: str) -> pd.DataFrame:
    """
    Faz download de dados públicos a partir de uma URL.
    Suporta CSV, JSON e JSONL.
    """
    url = _normalize_google_sheets_url(url)

    headers = {
        "User-Agent": "ETL-Pipeline/1.0",
        "Accept": "text/csv,application/json,*/*",
    }

    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()

    content_type = response.headers.get("content-type", "")

    # JSONL (linhas com JSON)
    lines = response.text.strip().splitlines()
    valid_json_lines = 0
    for line in lines[:20]:
        try:
            json.loads(line.strip())
            valid_json_lines += 1
        except Exception:
            pass
    if valid_json_lines >= min(5, len(lines)) and len(lines) > 1:
        return extract_from_jsonl(response.content)

    # JSON array
    if "json" in content_type:
        data = response.json()
        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict):
            for key in ("data", "results", "registros", "items", "records"):
                if key in data and isinstance(data[key], list):
                    return pd.DataFrame(data[key])
            return pd.DataFrame([data])

    # CSV
    try:
        df = pd.read_csv(io.StringIO(response.text), sep=None, engine="python")
        return df
    except Exception:
        pass

    # Último fallback: JSON
    try:
        data = json.loads(response.text)
        if isinstance(data, list):
            return pd.DataFrame(data)
        return pd.DataFrame([data])
    except Exception:
        pass

    raise ValueError(
        f"Não foi possível interpretar o conteúdo da URL. "
        f"Content-Type: {content_type}"
    )
