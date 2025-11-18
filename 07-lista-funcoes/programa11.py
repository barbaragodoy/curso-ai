
# 11. Crie uma função chamada filtrar_pares que receba uma lista de números
# inteiros e retorne uma nova lista contendo apenas os números pares.


def filtrar_pares(lista):
    """Retorna uma nova lista contendo apenas os números pares."""
    pares = []
    for numero in lista:
        if numero % 2 == 0:
            pares.append(numero)
    return pares


if __name__ == "__main__":
    # Programa principal
    numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    pares = filtrar_pares(numeros)
    print(f"Lista original: {numeros}")
    print(f"Números pares: {pares}")

