"""
Salva uma imagem no Redis como texto Base64 e recupera os bytes para um arquivo.

Requisitos:
  - Redis acessível (padrão: localhost:6379)
  - pip install -r requirements.txt

Uso:
  python salvar_recuperar_imagem_redis.py caminho\\para\\foto.png
  python salvar_recuperar_imagem_redis.py foto.png -o copia.png --chave minha:foto
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

import redis

CHAVE_PADRAO = "imagem:salva_base64"


def conectar(host: str, port: int) -> redis.Redis:
    return redis.Redis(host=host, port=port, decode_responses=True)


def salvar_imagem_base64(
    client: redis.Redis, chave: str, caminho_imagem: Path
) -> tuple[int, int]:
    """Lê a imagem, codifica em Base64, grava no Redis. Retorna (bytes originais, len base64)."""
    dados = caminho_imagem.read_bytes()
    texto_b64 = base64.b64encode(dados).decode("ascii")
    client.set(chave, texto_b64)
    return len(dados), len(texto_b64)


def recuperar_imagem_base64(client: redis.Redis, chave: str) -> bytes:
    """Lê Base64 do Redis e devolve os bytes binários da imagem."""
    texto = client.get(chave)
    if texto is None:
        raise KeyError(f"Chave inexistente ou expirada no Redis: {chave!r}")
    return base64.b64decode(texto, validate=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Armazena imagem no Redis (Base64) e recupera para arquivo via Python."
    )
    parser.add_argument(
        "imagem",
        type=Path,
        help="Caminho da imagem de entrada (PNG, JPG, etc.)",
    )
    parser.add_argument(
        "-o",
        "--saida",
        type=Path,
        default=None,
        help="Arquivo de saída da imagem recuperada (padrão: <nome>_recuperada<ext>)",
    )
    parser.add_argument(
        "--chave",
        default=CHAVE_PADRAO,
        help=f"Chave Redis (padrão: {CHAVE_PADRAO})",
    )
    parser.add_argument("--host", default="localhost", help="Host Redis")
    parser.add_argument("--port", type=int, default=6379, help="Porta Redis")

    args = parser.parse_args()
    entrada: Path = args.imagem

    if not entrada.is_file():
        print(f"Erro: arquivo não encontrado: {entrada}", file=sys.stderr)
        return 1

    try:
        client = conectar(args.host, args.port)
        client.ping()
    except redis.ConnectionError as exc:
        print(f"Erro: não foi possível conectar ao Redis ({args.host}:{args.port}): {exc}", file=sys.stderr)
        return 1

    print("--- Armazenamento ---")
    tam_bytes, tam_b64 = salvar_imagem_base64(client, args.chave, entrada)
    print(f"Chave Redis: {args.chave!r}")
    print(f"Bytes lidos do arquivo: {tam_bytes}")
    print(f"Tamanho da string Base64 armazenada: {tam_b64} caracteres")

    print("\n--- Recuperação ---")
    try:
        recuperados = recuperar_imagem_base64(client, args.chave)
    except (KeyError, ValueError) as exc:
        print(f"Erro ao recuperar/decodificar: {exc}", file=sys.stderr)
        return 1

    saida: Path = args.saida or entrada.with_name(
        f"{entrada.stem}_recuperada{entrada.suffix}"
    )
    saida.write_bytes(recuperados)
    print(f"Imagem recuperada gravada em: {saida.resolve()}")

    if recuperados == entrada.read_bytes():
        print("Verificação: conteúdo idêntico ao arquivo original.")
    else:
        print("Aviso: conteúdo recuperado difere do arquivo original.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
