# Programa 6: Imprimir todos os números múltiplos de 5, no intervalo fechado de 1 a 500
print("Múltiplos de 5 de 1 a 500:")
for i in range(1, 501):  # 1 a 500 (inclusive)
    if i % 5 == 0:  # Se é múltiplo de 5
        print(i)

