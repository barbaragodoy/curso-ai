# Programa 23: Calcular S = 1 + 1/2² + 1/3³ + 1/4⁴ + 1/5⁵ + ... + 1/N^N
N = int(input("Digite o valor de N: "))

if N <= 0:
    print("Erro: N deve ser positivo!")
else:
    S = 0
    print("Cálculo de S = 1 + 1/2² + 1/3³ + 1/4⁴ + 1/5⁵ + ... + 1/N^N")
    print("Termos:")
    
    for i in range(1, N + 1):
        termo = 1 / (i ** i)
        S += termo
        print(f"1/{i}^{i} = {termo:.6f}")
    
    print(f"\nS = {S:.6f}")

