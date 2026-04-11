#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import pymongo

# Conectar ao MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]
collection = db["funcionarios"]

# Limpar coleção anterior (opcional)
collection.delete_many({})

# URL da API
url = "https://randomuser.me/api/?results=10&nat=br"

# Fazer requisição
response = requests.get(url).json()

# Processar dados
funcionarios = []
for user in response["results"]:
    funcionarios.append({
        "nome": f"{user['name']['first']} {user['name']['last']}",
        "idade": user["dob"]["age"],
        "email": user["email"],
        "telefone": user["phone"],
        "cargo": "Desenvolvedor" if user["dob"]["age"] < 30 else "Gerente",
        "salario": 7000 if user["dob"]["age"] < 30 else 12000,
        "setor": "TI"
    })

# Inserir no MongoDB
collection.insert_many(funcionarios)
print("[OK] Dados inseridos com sucesso!")
print(f"Total de funcionarios: {collection.count_documents({})}")
