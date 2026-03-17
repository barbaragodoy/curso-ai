# Programa 20: Calcular H = 1 + 1/2 + 1/3 + 1/4 + ... + 1/N
N = int(input("Digite o valor de N: "))

if N <= 0:
    print("Erro: N deve ser positivo!")
else:
    H = 0
    print("Cálculo de H = 1 + 1/2 + 1/3 + ... + 1/N")
    print("Termos:")
    
    for i in range(1, N + 1):
        termo = 1 / i
        H += termo
        print(f"1/{i} = {termo:.6f}")
    
    print(f"\nH = {H:.6f}")

