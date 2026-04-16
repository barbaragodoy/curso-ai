# Exercício 9: Algoritmo que verifica se um número A é divisível por um número B

# Lê dois números do usuário
A = int(input("Digite o primeiro número (A): "))
B = int(input("Digite o segundo número (B): "))

# Verifica se A é divisível por B
if B == 0:
    print("Erro: Divisão por zero não é permitida.")
elif A % B == 0:
    print(f"O número {A} é divisível por {B}.")
else:
    print(f"O número {A} não é divisível por {B}.")
