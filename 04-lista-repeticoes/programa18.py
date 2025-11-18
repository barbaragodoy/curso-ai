# Programa 18: Gerar a série de Fibonacci até o N-ésimo termo
def fibonacci(n):
    """Gera a série de Fibonacci até o N-ésimo termo"""
    if n <= 0:
        return []
    elif n == 1:
        return [1]
    elif n == 2:
        return [1, 1]
    else:
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        return fib

N = int(input("Digite o número de termos da série de Fibonacci: "))
if N <= 0:
    print("Erro: O número deve ser positivo!")
else:
    serie = fibonacci(N)
    print(f"Série de Fibonacci com {N} termos:")
    for i, termo in enumerate(serie, 1):
        print(f"Termo {i}: {termo}")

