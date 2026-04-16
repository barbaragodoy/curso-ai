
# 4. Crie uma função contar_ocorrencias que receba uma lista de palavras e uma
# palavra específica, retornando o número de vezes que ela aparece na lista.



def contar_ocorrencias(lista_palavras, palavra):
    """Retorna o número de vezes que a palavra aparece na lista."""
    contador = 0
    for item in lista_palavras:
        if item == palavra:
            contador += 1
    return contador


if __name__ == "__main__":
    # Programa principal
    palavras = ["casa", "carro", "casa", "bicicleta", "casa", "moto"]
    palavra_busca = "casa"
    quantidade = contar_ocorrencias(palavras, palavra_busca)
    print(f"A palavra '{palavra_busca}' aparece {quantidade} vez(es) na lista.")

