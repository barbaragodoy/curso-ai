"""
Exemplos de comandos Redis executados via Python (redis-py).
Requisito: Redis em execução em localhost:6379.
"""

import base64
import time

import redis

# Quantidade de chaves no teste de escalabilidade (aumente com cuidado: muitas chaves = mais tempo e memória)
N_CHAVES_ESCALABILIDADE = 1000

# Conexão com o Redis (localhost). decode_responses=True devolve str em vez de bytes.
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

# ALTO DESEMPENHO
print("=== Testando Alto Desempenho ===")
start_time = time.time()

redis_client.set("chave_teste", "valor_teste")
retrieved_value = redis_client.get("chave_teste")

end_time = time.time()
print(f"Valor armazenado: {retrieved_value}")
print(f"Tempo de execução: {end_time - start_time:.6f} segundos\n")

# ESCALABILIDADE
print("=== Testando Escalabilidade ===")
for i in range(N_CHAVES_ESCALABILIDADE):
    redis_client.set(f"chave_{i}", f"valor_{i}")

exemplo_i = min(500, max(0, N_CHAVES_ESCALABILIDADE - 1))
print(f"Exemplo de valor armazenado: {redis_client.get(f'chave_{exemplo_i}')}\n")

# FLEXIBILIDADE
print("=== Testando Flexibilidade ===")

redis_client.set("string_exemplo", "Hello Redis!")
print(f"String armazenada: {redis_client.get('string_exemplo')}")

redis_client.rpush("lista_exemplo", "item1", "item2", "item3")
print(f"Lista armazenada: {redis_client.lrange('lista_exemplo', 0, -1)}")

redis_client.hset("hash_exemplo", "campo1", "valor1")
redis_client.hset("hash_exemplo", "campo2", "valor2")
print(f"Hash armazenado: {redis_client.hgetall('hash_exemplo')}")

image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8")
redis_client.set("imagem_binario", image_data)
img = redis_client.get("imagem_binario")
print(f"Imagem (binário armazenado): {img[:20]}... [Cortado]\n")

# BAIXA LATÊNCIA
print("=== Testando Baixa Latência ===")
redis_client.set("configuracao_cache", "config_inicial")
for _ in range(5):
    start_time = time.time()
    cache_value = redis_client.get("configuracao_cache")
    end_time = time.time()
    print(
        f"Cache acessado: {cache_value} | "
        f"Tempo de execução: {end_time - start_time:.6f} segundos"
    )

print("\nTeste concluído com sucesso!")
