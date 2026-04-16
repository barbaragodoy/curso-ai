#!/bin/bash

# Script de teste para PostgreSQL + pgAdmin

echo "============================================"
echo "TESTE DO AMBIENTE POSTGRESQL + PGADMIN"
echo "============================================"
echo ""

echo "[1] Status dos Containers"
docker compose ps
echo ""

echo "[2] Health Check do PostgreSQL"
docker compose ps | grep postgres_db
echo ""

echo "[3] Verificar conectividade do PostgreSQL"
docker exec postgres_db pg_isready -U admin
echo ""

echo "[4] Listar bases de dados"
docker exec -it postgres_db psql -U admin -d testdb -c "\l"
echo ""

echo "[5] Informações da Rede Docker"
docker network ls | grep postgres_network
docker network inspect postgresql-pgadmin-docker_postgres_network | grep -A 10 "Containers"
echo ""

echo "[6] Volumes"
docker volume ls | grep postgres_data
echo ""

echo "============================================"
echo "✓ Ambiente operacional!"
echo "✓ Acesse pgAdmin em: http://localhost:5050"
echo "✓ Credenciais: admin@example.com / admin123"
echo "✓ Conexão PostgreSQL: postgres_db:5432"
echo "============================================"
