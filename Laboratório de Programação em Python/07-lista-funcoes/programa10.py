
# 10. Escreva uma função linha_com_maior_soma que receba uma matriz e retorne
# o índice da linha que possui a maior soma dos seus elementos.



def linha_com_maior_soma(matriz):
    """Retorna o índice da linha com a maior soma dos seus elementos."""
    if len(matriz) == 0:
        return None
    
    maior_soma = sum(matriz[0])
    indice_maior = 0
    
    for i in range(1, len(matriz)):
        soma_linha = sum(matriz[i])
        if soma_linha > maior_soma:
            maior_soma = soma_linha
            indice_maior = i
    
    return indice_maior


if __name__ == "__main__":
    # Programa principal
    matriz = [
        [1, 2, 3],      # Soma: 6
        [4, 5, 6],      # Soma: 15
        [7, 8, 9],      # Soma: 24
        [1, 1, 1]       # Soma: 3
    ]
    resultado = linha_com_maior_soma(matriz)
    print(f"A linha com maior soma é a linha de índice: {resultado}")

