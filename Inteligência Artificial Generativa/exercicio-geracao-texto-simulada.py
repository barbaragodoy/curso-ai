"""
Inteligência Artificial Generativa - Exercício: Geração de texto (simulada)

Objetivo: Simular a ideia de geração autoregressiva: próximo token com base nos anteriores.
Em modelos reais (GPT, etc.) isso é feito por redes neurais; aqui usamos um dicionário simples.
"""

import random


def proxima_palavra(historico: list[str], regras: dict) -> str:
    """
    Dado o histórico de palavras, escolhe a próxima conforme regras (bigramas simulados).
    """
    if len(historico) < 1:
        return random.choice(list(regras.keys()))
    ultima = historico[-1]
    opcoes = regras.get(ultima, ["fim"])
    return random.choice(opcoes)


def gerar_frase(regras: dict, max_palavras: int = 10) -> str:
    """Gera uma sequência de palavras usando as regras (exemplo didático)."""
    frase = []
    for _ in range(max_palavras):
        prox = proxima_palavra(frase, regras)
        if prox == "fim":
            break
        frase.append(prox)
    return " ".join(frase)


if __name__ == "__main__":
    # "Modelo" mínimo: após cada palavra, quais podem vir em seguida
    bigramas = {
        "A": ["IA", "inteligência"],
        "IA": ["generativa", "muda"],
        "inteligência": ["artificial"],
        "artificial": ["generativa", "é"],
        "generativa": ["cria", "fim"],
        "cria": ["texto", "imagens"],
        "texto": ["e", "fim"],
        "e": ["imagens"],
        "imagens": ["fim"],
        "muda": ["o"],
        "o": ["mundo"],
        "é": ["incrível"],
        "incrível": ["fim"],
    }
    print("Geração de texto (simulada com bigramas):")
    for i in range(3):
        print(f"  Frase {i+1}:", gerar_frase(bigramas, 8))
