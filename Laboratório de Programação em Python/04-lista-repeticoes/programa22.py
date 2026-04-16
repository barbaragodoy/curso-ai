# Programa 22: Calcular S = 1/N + 2/(N-1) + 3/(N-2) + ... + (N-1)/2 + N/1
N = int(input("Digite o valor de N: "))

if N <= 0:
    print("Erro: N deve ser positivo!")
else:
    S = 0
    print("Cálculo de S = 1/N + 2/(N-1) + 3/(N-2) + ... + (N-1)/2 + N/1")
    print("Termos:")
    
    for i in range(1, N + 1):
        denominador = N - i + 1
        termo = i / denominador
        S += termo
        print(f"{i}/{denominador} = {termo:.6f}")
    
    print(f"\nS = {S:.6f}")

