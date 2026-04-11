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
print("EXEMPLOS DE AGREGACOES (AGGREGATE)")
print("=" * 70)

# Agregacao 1: Contar funcionários por cargo
print("\n[AGREGACAO 1] Contar funcionarios por cargo:")
print("Stage: {\"_id\": \"$cargo\", \"total_funcionarios\": {\"$sum\": 1}}")
result = list(collection.aggregate([
    {
        "$group": {
            "_id": "$cargo",
            "total_funcionarios": {"$sum": 1}
        }
    }
]))
for item in result:
    print(f"  - {item['_id']}: {item['total_funcionarios']} funcionarios")

# Agregacao 2: Média salarial por setor
print("\n[AGREGACAO 2] Media salarial por setor:")
print("Stage: {\"_id\": \"$setor\", \"media_salarial\": {\"$avg\": \"$salario\"}}")
result = list(collection.aggregate([
    {
        "$group": {
            "_id": "$setor",
            "media_salarial": {"$avg": "$salario"}
        }
    }
]))
for item in result:
    print(f"  - {item['_id']}: R${item['media_salarial']:.2f}")

# Agregacao 3: Maior idade por setor
print("\n[AGREGACAO 3] Maior idade por setor:")
print("Stage: {\"_id\": \"$setor\", \"maior_idade\": {\"$max\": \"$idade\"}}")
result = list(collection.aggregate([
    {
        "$group": {
            "_id": "$setor",
            "maior_idade": {"$max": "$idade"}
        }
    }
]))
for item in result:
    print(f"  - {item['_id']}: {item['maior_idade']} anos")

# Agregacao 4: Lista de funcionários por setor
print("\n[AGREGACAO 4] Lista de funcionarios por setor:")
print("Stage: {\"_id\": \"$setor\", \"nomes\": {\"$push\": \"$nome\"}}")
result = list(collection.aggregate([
    {
        "$group": {
            "_id": "$setor",
            "nomes": {"$push": "$nome"}
        }
    }
]))
for item in result:
    print(f"  - {item['_id']}: {', '.join(item['nomes'][:2])}... ({len(item['nomes'])} total)")

# Agregacao 5: Soma dos salários por cargo
print("\n[AGREGACAO 5] Soma dos salarios por cargo:")
print("Stage: {\"_id\": \"$cargo\", \"total_salario\": {\"$sum\": \"$salario\"}}")
result = list(collection.aggregate([
    {
        "$group": {
            "_id": "$cargo",
            "total_salario": {"$sum": "$salario"}
        }
    }
]))
for item in result:
    print(f"  - {item['_id']}: R${item['total_salario']}")
