
# 2. Crie uma função somar_elementos que receba uma lista de números e retorne
# a soma de todos os elementos.



def somar_elementos(lista):
    """Retorna a soma de todos os elementos da lista."""
    soma = 0
    for numero in lista:
        soma += numero
    return soma


if __name__ == "__main__":
    # Programa principal
    numeros = [10, 20, 30, 40, 50]
    resultado = somar_elementos(numeros)
    print(f"A soma dos elementos é: {resultado}")

