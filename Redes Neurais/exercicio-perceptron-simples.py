"""
Redes Neurais - Exercício: Perceptron simples

Objetivo: Implementar um perceptron (um neurônio) para classificação binária.
O perceptron aprende pesos w e bias b tal que y = ativação(w·x + b).
"""

import random


def degrau(z: float) -> int:
    """Função de ativação degrau: 1 se z >= 0, senão 0."""
    return 1 if z >= 0 else 0


def predizer(peso: list[float], bias: float, x: list[float]) -> int:
    """Calcula saída do perceptron para uma entrada x."""
    z = sum(w * xi for w, xi in zip(peso, x)) + bias
    return degrau(z)


def treinar_perceptron(
    X: list[list[float]], y: list[int], lr: float = 0.1, epocas: int = 50
) -> tuple[list[float], float]:
    """
    Ajusta pesos e bias com a regra do perceptron (classificação binária 0/1).
    """
    n_features = len(X[0])
    peso = [random.uniform(-0.5, 0.5) for _ in range(n_features)]
    bias = random.uniform(-0.5, 0.5)
    for _ in range(epocas):
        for xi, alvo in zip(X, y):
            pred = predizer(peso, bias, xi)
            erro = alvo - pred
            peso = [w + lr * erro * xi for w, xi in zip(peso, xi)]
            bias += lr * erro
    return peso, bias


if __name__ == "__main__":
    # AND lógico: (0,0)->0, (0,1)->0, (1,0)->0, (1,1)->1
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 0, 0, 1]
    peso, bias = treinar_perceptron(X, y)
    print("Perceptron treinado para porta AND:")
    print("  Pesos:", [round(w, 3) for w in peso], "| Bias:", round(bias, 3))
    for xi in X:
        print(f"  {xi} -> {predizer(peso, bias, xi)} (esperado: {y[X.index(xi)]})")
