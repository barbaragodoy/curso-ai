
# 6. Crie uma função exibir_matriz que receba uma lista de listas (matriz) e exiba
# seus elementos formatados como linhas e colunas.



def exibir_matriz(matriz):
    """Exibe os elementos da matriz formatados como linhas e colunas."""
    for linha in matriz:
        for elemento in linha:
            print(f"{elemento:4}", end=" ")
        print()  # Nova linha após cada linha da matriz


if __name__ == "__main__":
    # Programa principal
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    exibir_matriz(matriz)

