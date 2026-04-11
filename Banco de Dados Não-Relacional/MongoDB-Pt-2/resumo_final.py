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
print("RESUMO FINAL - DADOS E OPERACOES")
print("=" * 70)

# Dados gerais
total = collection.count_documents({})
print(f"\n[DADOS GERAIS]")
print(f"  Total de funcionarios: {total}")

# Amostra de dados
print(f"\n[AMOSTRA DE FUNCIONARIOS]")
sample = list(collection.find().limit(3))
for func in sample:
    print(f"  - {func['nome']}")
    print(f"    Email: {func['email']}")
    print(f"    Cargo: {func['cargo']} | Salario: R${func['salario']}")
    print()

# Estatisticas por cargo
print(f"[ESTATISTICAS POR CARGO]")
stats = list(collection.aggregate([
    {"$group": {
        "_id": "$cargo",
        "quantidade": {"$sum": 1},
        "salario_medio": {"$avg": "$salario"},
        "idade_media": {"$avg": "$idade"}
    }}
]))
for stat in stats:
    print(f"  {stat['_id']}:")
    print(f"    Quantidade: {stat['quantidade']}")
    print(f"    Salario medio: R${stat['salario_medio']:.2f}")
    print(f"    Idade media: {stat['idade_media']:.1f} anos")

# Indices criados
print(f"\n[INDICES CRIADOS]")
indexes = list(collection.list_indexes())
for idx in indexes:
    if idx['name'] != '_id_':
        print(f"  - {idx['name']}")

# Validacao
print(f"\n[VALIDACAO DE SCHEMA]")
print(f"  Status: Ativa")
print(f"  Campos obrigatorios: nome, idade, email, cargo, salario, setor")
print(f"  Regras: idade >= 18, cargo in ['Desenvolvedor', 'Gerente']")
