
# 15. Crie uma função matriz_identidade(n) que receba um número inteiro n e
# retorne uma matriz identidade de ordem n.



def matriz_identidade(n):
    """Retorna uma matriz identidade de ordem n."""
    if n <= 0:
        raise ValueError("O valor de n deve ser um inteiro positivo.")
    
    matriz = []
    for i in range(n):
        linha = []
        for j in range(n):
            if i == j:
                linha.append(1)
            else:
                linha.append(0)
        matriz.append(linha)
    return matriz


if __name__ == "__main__":
    # Programa principal
    n = 4
    identidade = matriz_identidade(n)
    print(f"Matriz identidade de ordem {n}:")
    for linha in identidade:
        print(linha)

