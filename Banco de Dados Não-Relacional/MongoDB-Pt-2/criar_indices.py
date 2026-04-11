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
print("CRIACAO DE INDICES")
print("=" * 70)

# Indice 1: Unico em email
print("\n[INDICE 1] Indice UNICO em email:")
print("Field: email | Type: 1 (asc) | Unique: True")
try:
    collection.create_index("email", unique=True)
    print("[OK] Indice criado!")
    
    # Testar query
    result = collection.find_one({"email": collection.find_one()["email"]})
    print(f"Query test: {result['nome']} ({result['email']})")
except Exception as e:
    print(f"Indice ja existe: {e}")

# Indice 2: Texto em nome e cargo
print("\n[INDICE 2] Indice TEXT em nome e cargo:")
print("Field 1: nome | Type: text")
print("Field 2: cargo | Type: text")
try:
    collection.create_index([("nome", "text"), ("cargo", "text")])
    print("[OK] Indice criado!")
    
    # Testar query
    result = list(collection.find({"$text": {"$search": "Desenvolvedor"}}))
    print(f"Query test: {len(result)} resultado(s) para 'Desenvolvedor'")
    if result:
        print(f"  - {result[0]['nome']} | {result[0]['cargo']}")
except Exception as e:
    print(f"Indice ja existe: {e}")

# Indice 3: Parcial em salario (salario >= 7000)
print("\n[INDICE 3] Indice PARCIAL em salario (>= 7000):")
print("Field: salario | Type: 1 (asc)")
print("Partial Filter: {\"salario\": {\"$gte\": 7000}}")
try:
    collection.create_index("salario", partialFilterExpression={"salario": {"$gte": 7000}})
    print("[OK] Indice criado!")
    
    # Testar query
    result = list(collection.find({"salario": {"$gte": 7000}}))
    print(f"Query test: {len(result)} funcionarios com salario >= R$7000")
except Exception as e:
    print(f"Indice ja existe: {e}")

# Listar todos os indices
print("\n[INDICES EXISTENTES]")
indexes = collection.list_indexes()
for idx in indexes:
    print(f"  - {idx['name']}: {idx['key']}")
