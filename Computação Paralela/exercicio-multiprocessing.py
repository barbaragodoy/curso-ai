"""
Computação Paralela - Exercício: Multiprocessing

Objetivo: Processar tarefas em paralelo usando multiprocessing.
Cada processo roda em um núcleo diferente, aproveitando CPU multi-core.
"""

import multiprocessing
import time


def tarefa_pesada(n: int) -> int:
    """Simula um cálculo (ex.: soma de 1 até n)."""
    return sum(range(n))


def main_paralelo():
    """Executa várias tarefas em processos paralelos."""
    valores = [5_000_000, 6_000_000, 7_000_000]
    inicio = time.perf_counter()
    with multiprocessing.Pool(processes=3) as pool:
        resultados = pool.map(tarefa_pesada, valores)
    fim = time.perf_counter()
    print("Resultados:", resultados)
    print(f"Tempo paralelo: {fim - inicio:.3f}s")
    return resultados


def main_sequencial():
    """Mesmas tarefas em sequência (para comparação)."""
    valores = [5_000_000, 6_000_000, 7_000_000]
    inicio = time.perf_counter()
    resultados = [tarefa_pesada(v) for v in valores]
    fim = time.perf_counter()
    print("Resultados:", resultados)
    print(f"Tempo sequencial: {fim - inicio:.3f}s")
    return resultados


if __name__ == "__main__":
    print("=== Execução sequencial ===")
    main_sequencial()
    print("\n=== Execução paralela (multiprocessing) ===")
    main_paralelo()
