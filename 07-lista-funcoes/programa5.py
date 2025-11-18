
# 5. Escreva uma função chamada maior_valor que receba uma lista de números e
# retorne o maior valor contido nela.



def maior_valor(lista):
    """Retorna o maior valor da lista."""
    if len(lista) == 0:
        return None
    
    maior = lista[0]
    for numero in lista:
        if numero > maior:
            maior = numero
    return maior


if __name__ == "__main__":
    # Programa principal
    numeros = [15, 8, 23, 4, 42, 11, 19]
    resultado = maior_valor(numeros)
    print(f"O maior valor da lista é: {resultado}")

