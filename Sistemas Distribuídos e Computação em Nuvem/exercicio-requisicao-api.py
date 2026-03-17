"""
Sistemas Distribuídos e Computação em Nuvem - Exercício: Requisições e APIs

Objetivo: Consumir um serviço remoto (API) como em sistemas distribuídos.
Exemplo com API pública (JSONPlaceholder) ou simulação local.
"""

# Para usar API real: pip install requests
# import requests

import json
import urllib.request
import urllib.error


def buscar_api_publica(url: str) -> dict | None:
    """
    Faz GET em uma URL e retorna o JSON parseado.
    Usa apenas biblioteca padrão (urllib).
    """
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            dados = json.loads(resp.read().decode())
            return dados
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as e:
        print(f"Erro ao acessar API: {e}")
        return None


def simular_resposta_api():
    """Simula resposta de uma API (útil se estiver offline)."""
    return {
        "userId": 1,
        "id": 1,
        "title": "Título de exemplo (simulado)",
        "body": "Corpo da publicação. Em sistemas distribuídos, serviços se comunicam via APIs.",
    }


if __name__ == "__main__":
    # API pública de exemplo (posts)
    url = "https://jsonplaceholder.typicode.com/posts/1"
    print("Requisição GET (ex.: serviço na nuvem):", url)
    dados = buscar_api_publica(url)
    if dados:
        print("Resposta:", json.dumps(dados, indent=2, ensure_ascii=False))
    else:
        print("Resposta (simulada):", json.dumps(simular_resposta_api(), indent=2, ensure_ascii=False))
