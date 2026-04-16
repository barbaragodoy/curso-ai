
# 13. Escreva uma função remover_duplicatas que receba uma lista com possíveis
# elementos repetidos e retorne uma nova lista sem repetições.



def remover_duplicatas(lista):
    """Retorna uma nova lista sem elementos repetidos."""
    lista_sem_duplicatas = []
    for elemento in lista:
        if elemento not in lista_sem_duplicatas:
            lista_sem_duplicatas.append(elemento)
    return lista_sem_duplicatas


if __name__ == "__main__":
    # Programa principal
    lista_com_duplicatas = [1, 2, 2, 3, 4, 4, 4, 5, 1, 3]
    lista_sem_duplicatas = remover_duplicatas(lista_com_duplicatas)
    print(f"Lista original: {lista_com_duplicatas}")
    print(f"Lista sem duplicatas: {lista_sem_duplicatas}")

