
# 9. Crie uma função soma_total_matriz que receba uma matriz com números
# inteiros e retorne a soma de todos os valores.


def soma_total_matriz(matriz):
    """Retorna a soma de todos os valores da matriz."""
    soma_total = 0
    for linha in matriz:
        for valor in linha:
            soma_total += valor
    return soma_total


if __name__ == "__main__":
    # Programa principal
    matriz = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    resultado = soma_total_matriz(matriz)
    print(f"A soma total da matriz é: {resultado}")

