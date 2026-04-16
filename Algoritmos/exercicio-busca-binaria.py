"""
Algoritmos - Exercício: Busca binária

Objetivo: Implementar busca binária em uma lista ordenada.
A busca binária divide o espaço de busca pela metade a cada comparação (O(log n)).
"""


def busca_binaria(lista: list, alvo: int) -> int:
    """
    Retorna o índice do alvo na lista ordenada, ou -1 se não existir.
    """
    esquerda, direita = 0, len(lista) - 1
    while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if lista[meio] == alvo:
            return meio
        if lista[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    return -1


if __name__ == "__main__":
    dados = [2, 5, 8, 12, 16, 23, 38, 45, 67]
    valor = 23
    pos = busca_binaria(dados, valor)
    print(f"Lista: {dados}")
    print(f"Busca por {valor}: índice {pos}")
    if pos >= 0:
        print(f"Encontrado na posição {pos}.")
    else:
        print("Valor não encontrado.")
