# Programa 21: Calcular H = 1 - 1/2 + 1/3 - 1/4 + ... + 1/N (alternando sinais)
N = int(input("Digite o valor de N: "))

if N <= 0:
    print("Erro: N deve ser positivo!")
else:
    H = 0
    print("Cálculo de H = 1 - 1/2 + 1/3 - 1/4 + ... + 1/N")
    print("Termos:")
    
    for i in range(1, N + 1):
        if i % 2 == 1:  # Termos ímpares são positivos
            termo = 1 / i
            sinal = "+"
        else:  # Termos pares são negativos
            termo = -1 / i
            sinal = "-"
        
        H += termo
        print(f"{sinal}1/{i} = {termo:.6f}")
    
    print(f"\nH = {H:.6f}")

