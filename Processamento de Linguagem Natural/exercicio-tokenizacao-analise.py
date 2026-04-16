"""
Processamento de Linguagem Natural (PLN) - Exercício: Tokenização e análise simples

Objetivo: Dividir texto em tokens (palavras) e extrair informações básicas.
Em projetos reais use NLTK, spaCy ou transformers.
"""

import re


def tokenizar(texto: str) -> list[str]:
    """Divide o texto em palavras (minúsculas), removendo pontuação."""
    texto_limpo = re.sub(r"[^\w\sáéíóúãõâêîôûàèìòù]", "", texto.lower())
    return texto_limpo.split()


def contar_palavras(tokens: list[str]) -> dict[str, int]:
    """Contagem de frequência de cada palavra."""
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq


def palavras_mais_frequentes(freq: dict, top_n: int = 5) -> list[tuple[str, int]]:
    """Retorna as top_n palavras mais frequentes."""
    ordenado = sorted(freq.items(), key=lambda x: -x[1])
    return ordenado[:top_n]


if __name__ == "__main__":
    frase = "A inteligência artificial e o processamento de linguagem natural mudam o mundo. A IA avança."
    tokens = tokenizar(frase)
    freq = contar_palavras(tokens)
    top = palavras_mais_frequentes(freq, 5)
    print("Texto:", frase)
    print("Tokens:", tokens)
    print("Frequência:", freq)
    print("Top 5 palavras:", top)
