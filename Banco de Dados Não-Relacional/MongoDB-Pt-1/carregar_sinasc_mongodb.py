"""
Atividade MongoDB (Pt-1): carregar CSV SINASC no MongoDB, consultar e amostrar com Pandas.

Pré-requisitos:
  - MongoDB em execução (local: mongodb://localhost:27018).
  - pip install -r requirements.txt

Evidência no Compass: conecte com a mesma URI usada aqui, abra o database SINASC_PT1,
  collection nascimentos_2020, e faça um print da tela completa (incluindo a barra de tarefas).

Autenticação: se aparecer "requires authentication", defina a URI antes de rodar, por exemplo:
  PowerShell: $env:MONGO_URI = "mongodb://USUARIO:SENHA@localhost:27017/?authSource=admin"

Uso:
  python carregar_sinasc_mongodb.py              # carrega se a coleção estiver vazia; depois consulta
  python carregar_sinasc_mongodb.py --recarregar # esvazia a coleção e importa o CSV de novo
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, OperationFailure


# Caminho padrão: mesmo diretório do script
CSV_PADRAO = Path(__file__).resolve().parent / "SINASC_2020_10pct.csv"

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27018/")
DATABASE = os.environ.get("MONGO_DB", "SINASC_PT1")
COLLECTION_NAME = os.environ.get("MONGO_COLLECTION", "nascimentos_2020")

CHUNK_ROWS = 5000


def _limpar_valor(v):
    if pd.isna(v):
        return None
    return v


def registros_do_chunk(df: pd.DataFrame) -> list[dict]:
    """Converte um DataFrame em lista de dicts compatível com BSON (sem NaN)."""
    df = df.copy()
    registros = []
    for row in df.to_dict(orient="records"):
        registros.append({k: _limpar_valor(v) for k, v in row.items()})
    return registros


def carregar_csv_na_colecao(
    caminho_csv: Path,
    collection: Collection,
    recarregar: bool,
) -> int:
    if recarregar:
        # delete_many costuma exigir o mesmo nível de permissão que drop; evita erro se a coleção não existir
        collection.delete_many({})

    if collection.estimated_document_count() > 0:
        return 0

    total = 0
    for chunk in pd.read_csv(
        caminho_csv,
        sep=";",
        encoding="latin-1",
        dtype=str,
        chunksize=CHUNK_ROWS,
        low_memory=False,
    ):
        docs = registros_do_chunk(chunk)
        if docs:
            collection.insert_many(docs, ordered=False)
            total += len(docs)
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description="Importa SINASC (CSV) para MongoDB e exibe amostras.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=CSV_PADRAO,
        help="Caminho do arquivo CSV (padrão: SINASC_2020_10pct.csv na pasta do script).",
    )
    parser.add_argument(
        "--recarregar",
        action="store_true",
        help="Esvazia a coleção e importa o CSV novamente.",
    )
    args = parser.parse_args()

    if not args.csv.is_file():
        raise SystemExit(f"Arquivo não encontrado: {args.csv}")

    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
        db = client[DATABASE]
        coll = db[COLLECTION_NAME]
        # força checagem de conexão/autenticação cedo
        client.admin.command("ping")
    except ConnectionFailure as e:
        raise SystemExit(
            "Não foi possível alcançar o MongoDB (serviço parado, porta errada ou firewall).\n"
            f"Detalhe: {e}"
        ) from e
    except OperationFailure as e:
        raise SystemExit(
            "Falha ao conectar/autenticar no MongoDB. Ajuste MONGO_URI (usuário, senha, authSource).\n"
            f"Detalhe: {e}"
        ) from e

    try:
        inseridos = carregar_csv_na_colecao(args.csv, coll, args.recarregar)
    except OperationFailure as e:
        raise SystemExit(
            "Sem permissão para inserir ou limpar a coleção. Verifique usuário/roles no MongoDB.\n"
            f"Detalhe: {e}"
        ) from e
    if inseridos:
        print(f"Inseridos {inseridos} documentos em {DATABASE}.{COLLECTION_NAME}.")
    elif not args.recarregar:
        print(
            f"Coleção já continha dados; nada foi inserido. "
            f"Use --recarregar para reimportar o CSV."
        )

    total = coll.estimated_document_count()
    print(f"Total de documentos na coleção: {total}\n")

    # Colunas úteis para leitura no terminal (subset do SINASC)
    cols_destaque = [
        "DTNASC",
        "SEXO",
        "PESO",
        "IDADEMAE",
        "CODMUNNASC",
        "LOCNASC",
        "PARTO",
        "GESTACAO",
    ]

    # Amostra direto do MongoDB (primeiros documentos, ordem natural)
    cursor = coll.find({}, limit=10)
    amostra = list(cursor)
    print("--- Até 10 documentos (consulta no MongoDB) — trechos dos campos ---")
    for i, doc in enumerate(amostra, start=1):
        trecho = {c: doc.get(c) for c in cols_destaque if c in doc}
        print(f"[{i}] _id={doc.get('_id')!s} {trecho}")

    # 5 amostras com Pandas (a partir dos dados lidos do banco)
    df = pd.DataFrame(amostra)
    if "_id" in df.columns:
        df["_id"] = df["_id"].astype(str)

    print("\n--- 5 linhas (Pandas) — colunas em destaque dos primeiros documentos ---")
    n = min(5, len(df))
    if n == 0:
        print("(Nenhum documento para exibir.)")
    else:
        existentes = [c for c in cols_destaque if c in df.columns]
        cols_df = (existentes + ["_id"]) if "_id" in df.columns else existentes
        print(df.loc[:, [c for c in cols_df if c in df.columns]].head(n).to_string())

    print("\n--- 5 linhas aleatórias (Pandas sample), se houver pelo menos 5 na coleção ---")
    if total >= 5:
        aleatorios = list(coll.aggregate([{"$sample": {"size": 5}}]))
        df_rand = pd.DataFrame(aleatorios)
        if "_id" in df_rand.columns:
            df_rand["_id"] = df_rand["_id"].astype(str)
        existentes_r = [c for c in cols_destaque if c in df_rand.columns]
        cols_r = (existentes_r + ["_id"]) if "_id" in df_rand.columns else existentes_r
        print(df_rand.loc[:, [c for c in cols_r if c in df_rand.columns]].to_string())
    else:
        print("(Coleção com menos de 5 documentos; sample de 5 não aplicável.)")

    client.close()
    print(f"\nConexão: {MONGO_URI!r} | Database: {DATABASE!r} | Collection: {COLLECTION_NAME!r}")


if __name__ == "__main__":
    main()
