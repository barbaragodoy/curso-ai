"""
Banco de Dados Não-Relacional - Exercício: Documentos e JSON

Objetivo: Simular armazenamento e consulta no estilo documento (ex.: MongoDB).
Usamos listas e dicionários em Python para representar documentos.
"""

import json


def criar_documento(nome: str, idade: int, cursos: list) -> dict:
    """Cria um documento no formato chave-valor (estilo documento)."""
    return {
        "nome": nome,
        "idade": idade,
        "cursos": cursos,
    }


def buscar_por_idade(documentos: list[dict], idade_min: int) -> list[dict]:
    """Consulta simulada: documentos com idade >= idade_min."""
    return [doc for doc in documentos if doc["idade"] >= idade_min]


if __name__ == "__main__":
    # "Coleção" de documentos (em um BD real seria uma collection)
    colecao = [
        criar_documento("Ana", 22, ["Python", "IA"]),
        criar_documento("Bruno", 19, ["BD", "Redes"]),
        criar_documento("Carla", 25, ["IA", "ML"]),
    ]
    print("Documentos (JSON):")
    print(json.dumps(colecao, indent=2, ensure_ascii=False))
    print("\nConsulta: idade >= 22")
    resultado = buscar_por_idade(colecao, 22)
    for doc in resultado:
        print(" -", doc["nome"], doc["idade"], doc["cursos"])
