
# 3. Implemente uma função buscar_elemento que receba uma lista e um valor. A
# função deve verificar se o valor está na lista e retornar uma mensagem apropriada.



def buscar_elemento(lista, valor):
    """Verifica se o valor está na lista e retorna uma mensagem apropriada."""
    if valor in lista:
        return f"O valor '{valor}' foi encontrado na lista."
    else:
        return f"O valor '{valor}' não foi encontrado na lista."


if __name__ == "__main__":
    # Programa principal
    minha_lista = [1, 2, 3, 4, 5]
    resultado1 = buscar_elemento(minha_lista, 3)
    resultado2 = buscar_elemento(minha_lista, 10)
    print(resultado1)
    print(resultado2)

