"""
Visão Computacional - Exercício: Processamento de imagem (estrutura)

Objetivo: Estrutura base para trabalhar com imagens (carregar, dimensões, pixels).
Em projetos reais use OpenCV (cv2) ou Pillow (PIL). Aqui simulamos com uma matriz 2D.
"""

# Descomente quando instalar: pip install pillow
# from PIL import Image
# import numpy as np  # pip install numpy


def criar_imagem_simulada(altura: int, largura: int) -> list[list[int]]:
    """
    Cria uma "imagem" como matriz de intensidades (0-255).
    Simula um gradiente simples para exercício.
    """
    return [
        [(i + j) % 256 for j in range(largura)]
        for i in range(altura)
    ]


def dimensoes_imagem(imagem: list[list]) -> tuple[int, int]:
    """Retorna (altura, largura) da imagem."""
    return len(imagem), len(imagem[0]) if imagem else 0


def valor_medio(imagem: list[list[int]]) -> float:
    """Calcula valor médio dos pixels (brilho médio)."""
    total = sum(sum(linha) for linha in imagem)
    n = dimensoes_imagem(imagem)[0] * dimensoes_imagem(imagem)[1]
    return total / n if n else 0


if __name__ == "__main__":
    # Imagem simulada 4x5 (em prática use: img = np.array(Image.open("foto.jpg")))
    img = criar_imagem_simulada(4, 5)
    h, w = dimensoes_imagem(img)
    print("Visão Computacional - Processamento de imagem (estrutura)")
    print("Dimensões (altura x largura):", h, "x", w)
    print("Matriz de intensidades (amostra):")
    for linha in img[:2]:
        print(" ", linha)
    print("Brilho médio (valor médio dos pixels):", round(valor_medio(img), 2))
    print("\nPara imagens reais: use PIL (Image.open) ou OpenCV (cv2.imread).")
