
#12. Implemente uma função inverter_lista que receba uma lista e retorne a lista
# invertida (sem usar o método reverse() ou [::-1]).



def inverter_lista(lista):
    """Retorna a lista invertida sem usar reverse() ou [::-1]."""
    lista_invertida = []
    for i in range(len(lista) - 1, -1, -1):
        lista_invertida.append(lista[i])
    return lista_invertida


if __name__ == "__main__":
    # Programa principal
    lista_original = [1, 2, 3, 4, 5]
    lista_invertida = inverter_lista(lista_original)
    print(f"Lista original: {lista_original}")
    print(f"Lista invertida: {lista_invertida}")

