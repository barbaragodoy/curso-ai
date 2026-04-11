#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]
collection = db["funcionarios"]

print("=" * 70)
print("EXEMPLOS DE CONSULTAS (FIND)")
print("=" * 70)

# Consulta 1: Buscar todos os funcionários do setor de TI
print("\n[CONSULTA 1] Todos os funcionarios do setor TI:")
print("Query: {\"setor\": \"TI\"}")
result = list(collection.find({"setor": "TI"}))
for func in result[:3]:
    print(f"  - {func['nome']} | {func['cargo']} | R${func['salario']}")
if len(result) > 3:
    print(f"  ... e mais {len(result)-3}")

# Consulta 2: Encontrar funcionários com salário maior que R$ 10.000
print("\n[CONSULTA 2] Funcionarios com salario > R$ 10.000:")
print("Query: {\"salario\": {\"$gt\": 10000}}")
result = list(collection.find({"salario": {"$gt": 10000}}))
for func in result:
    print(f"  - {func['nome']} | {func['cargo']} | R${func['salario']}")

# Consulta 3: Buscar apenas os funcionários que são gerentes
print("\n[CONSULTA 3] Apenas Gerentes:")
print("Query: {\"cargo\": \"Gerente\"}")
result = list(collection.find({"cargo": "Gerente"}))
for func in result:
    print(f"  - {func['nome']} | Idade: {func['idade']} | R${func['salario']}")

# Consulta 4: Buscar funcionários com idade entre 25 e 35 anos
print("\n[CONSULTA 4] Funcionarios com idade entre 25 e 35 anos:")
print("Query: {\"idade\": {\"$gte\": 25, \"$lte\": 35}}")
result = list(collection.find({"idade": {"$gte": 25, "$lte": 35}}))
for func in result:
    print(f"  - {func['nome']} | {func['idade']} anos | {func['cargo']}")
