# Programa 19: Série de Ricci - dois primeiros termos fornecidos pelo usuário
def serie_ricci(termo1, termo2, n):
    """Gera a série de Ricci com os primeiros dois termos fornecidos"""
    if n < 3:
        return "Erro: Para existir a série de Ricci são necessários pelo menos 3 termos!"
    
    ricci = [termo1, termo2]
    for i in range(2, n):
        ricci.append(ricci[i-1] + ricci[i-2])
    
    return ricci

# Entrada dos dados
termo1 = float(input("Digite o primeiro termo da série de Ricci: "))
termo2 = float(input("Digite o segundo termo da série de Ricci: "))
N = int(input("Digite quantos termos da série de Ricci você quer: "))

if N < 3:
    print("Erro: Para existir a série de Ricci são necessários pelo menos 3 termos!")
else:
    serie = serie_ricci(termo1, termo2, N)
    print(f"Série de Ricci com {N} termos:")
    soma = 0
    for i, termo in enumerate(serie, 1):
        print(f"Termo {i}: {termo}")
        soma += termo
    
    print(f"Soma dos termos: {soma}")

