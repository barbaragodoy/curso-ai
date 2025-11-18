
# 7. Desenvolva uma função somar_coluna que receba uma matriz (lista de listas) e
# o índice de uma coluna. A função deve retornar a soma dos valores dessa coluna.



def somar_coluna(matriz, indice_coluna):
    """Retorna a soma dos valores da coluna especificada."""
    soma = 0
    for linha in matriz:
        if indice_coluna < len(linha):
            soma += linha[indice_coluna]
    return soma


if __name__ == "__main__":
    # Programa principal
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    coluna = 1  # Segunda coluna (índice 1)
    resultado = somar_coluna(matriz, coluna)
    print(f"A soma da coluna {coluna} é: {resultado}")

