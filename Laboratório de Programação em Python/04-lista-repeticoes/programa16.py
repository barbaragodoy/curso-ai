# Programa 16: Calcular o fatorial de um número N
def fatorial(n):
    """Calcula o fatorial de um número"""
    if n < 0:
        return "Erro: Fatorial não definido para números negativos"
    elif n == 0 or n == 1:
        return 1
    else:
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado

N = int(input("Digite um número para calcular o fatorial: "))
resultado = fatorial(N)
print(f"{N}! = {resultado}")

