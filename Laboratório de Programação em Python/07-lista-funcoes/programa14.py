
# 14. Desenvolva uma função media_por_linha que receba uma matriz numérica e
# retorne uma lista com a média de cada linha.



def media_por_linha(matriz):
    """Retorna uma lista com a média de cada linha da matriz."""
    medias = []
    for linha in matriz:
        if len(linha) > 0:
            media = sum(linha) / len(linha)
            medias.append(media)
        else:
            medias.append(0)
    return medias


if __name__ == "__main__":
    # Programa principal
    matriz = [
        [1, 2, 3],      # Média: 2.0
        [4, 5, 6],      # Média: 5.0
        [7, 8, 9, 10]   # Média: 8.5
    ]
    medias = media_por_linha(matriz)
    print("Médias por linha:")
    for i, media in enumerate(medias):
        print(f"Linha {i}: {media:.2f}")

