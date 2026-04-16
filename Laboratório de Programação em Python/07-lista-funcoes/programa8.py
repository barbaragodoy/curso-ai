
# 8. Implemente uma função buscar_em_matriz que receba uma matriz e um valor,
# e informe se o valor está presente em alguma posição da matriz.



def buscar_em_matriz(matriz, valor):
    """Verifica se o valor está presente em alguma posição da matriz."""
    for linha in matriz:
        if valor in linha:
            return f"O valor {valor} foi encontrado na matriz."
    return f"O valor {valor} não foi encontrado na matriz."


if __name__ == "__main__":
    # Programa principal
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    resultado1 = buscar_em_matriz(matriz, 5)
    resultado2 = buscar_em_matriz(matriz, 10)
    print(resultado1)
    print(resultado2)

