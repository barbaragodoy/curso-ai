
#1. Crie uma função chamada mostrar_lista que receba uma lista como parâmetro
# e exiba cada elemento em uma nova linha. No programa principal, crie uma lista
# com cinco nomes e chame a função.


def mostrar_lista(lista):
    """Exibe cada elemento da lista em uma nova linha."""
    for elemento in lista:
        print(elemento)


if __name__ == "__main__":
    # Programa principal
    nomes = ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"]
    mostrar_lista(nomes)

