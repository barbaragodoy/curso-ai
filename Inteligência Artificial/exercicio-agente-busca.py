"""
Inteligência Artificial - Exercício: Agente e busca simples

Objetivo: Simular um agente que toma decisões em um ambiente (grafo).
Exemplo: busca em largura (BFS) para encontrar caminho entre nós.
"""

from collections import deque


def busca_em_largura(grafo: dict, inicio: str, objetivo: str) -> list | None:
    """
    Retorna um caminho do nó inicio ao objetivo, ou None se não existir.
    """
    fila = deque([[inicio]])
    visitados = {inicio}
    while fila:
        caminho = fila.popleft()
        no = caminho[-1]
        if no == objetivo:
            return caminho
        for vizinho in grafo.get(no, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(caminho + [vizinho])
    return None


if __name__ == "__main__":
    # Grafo simples: cidade -> cidades vizinhas
    mapa = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    caminho = busca_em_largura(mapa, "A", "F")
    print("Grafo (ex.: mapa de cidades):", mapa)
    print("Caminho de A até F (BFS):", caminho)
