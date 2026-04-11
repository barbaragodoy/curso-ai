#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["startup"]

# Validacao de schema
validation_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nome", "idade", "email", "cargo", "salario", "setor"],
        "properties": {
            "nome": {
                "bsonType": "string",
                "description": "O nome deve ser uma string."
            },
            "idade": {
                "bsonType": "int",
                "minimum": 18,
                "description": "A idade deve ser um numero inteiro maior ou igual a 18."
            },
            "email": {
                "bsonType": "string",
                "pattern": "^.+@.+..+$",
                "description": "O email deve ser um endereco valido."
            },
            "cargo": {
                "bsonType": "string",
                "enum": ["Desenvolvedor", "Gerente"],
                "description": "O cargo deve ser 'Desenvolvedor' ou 'Gerente'."
            },
            "salario": {
                "bsonType": "int",
                "minimum": 0,
                "description": "O salario deve ser um numero inteiro positivo."
            },
            "setor": {
                "bsonType": "string",
                "description": "O setor deve ser uma string."
            }
        }
    }
}

print("=" * 70)
print("APLICANDO VALIDACAO DE SCHEMA JSON")
print("=" * 70)

try:
    db.command("collMod", "funcionarios", validator=validation_schema)
    print("\n[OK] Validacao de schema aplicada com sucesso!")
except Exception as e:
    print(f"\n[ERRO] {e}")

# Testar validacao - teste invalido
print("\n[TESTE 1] Tentando inserir funcionario COM IDADE INVALIDA (< 18):")
try:
    db.funcionarios.insert_one({
        "nome": "Teste Invalido",
        "idade": 15,
        "email": "teste@example.com",
        "cargo": "Desenvolvedor",
        "salario": 7000,
        "setor": "TI"
    })
    print("[FALHA] Documento foi inserido (schema nao foi validado)")
except Exception as e:
    print(f"[OK] Insercao bloqueada: {str(e)[:100]}...")

# Testar validacao - teste invalido
print("\n[TESTE 2] Tentando inserir com CARGO INVALIDO:")
try:
    db.funcionarios.insert_one({
        "nome": "Teste Invalido",
        "idade": 25,
        "email": "teste2@example.com",
        "cargo": "Diretor",
        "salario": 7000,
        "setor": "TI"
    })
    print("[FALHA] Documento foi inserido")
except Exception as e:
    print(f"[OK] Insercao bloqueada: {str(e)[:100]}...")

# Testar validacao - teste valido
print("\n[TESTE 3] Inserindo funcionario VALIDO:")
try:
    db.funcionarios.insert_one({
        "nome": "João Silva",
        "idade": 28,
        "email": "joao.silva@example.com",
        "cargo": "Desenvolvedor",
        "salario": 7500,
        "setor": "TI"
    })
    print("[OK] Funcionario inserido com sucesso!")
    
    # Verificar total
    total = db.funcionarios.count_documents({})
    print(f"Total de funcionarios agora: {total}")
except Exception as e:
    print(f"[ERRO] {e}")
