# PostgreSQL + pgAdmin com Docker Compose

Ambiente containerizado com **PostgreSQL 16** e **pgAdmin 4** para gerenciamento de banco de dados.

## 🚀 Iniciar o Ambiente

```bash
docker compose up -d
```

## 📊 Acessar pgAdmin

- **URL:** http://localhost:5050
- **Email:** admin@example.com
- **Senha:** admin123

## 🗄️ Conexão com PostgreSQL

Dentro do pgAdmin, criar novo servidor com:
- **Hostname:** postgres_db
- **Port:** 5432
- **Username:** admin
- **Password:** admin123
- **Database:** testdb

## 📋 Status dos Containers

```bash
docker compose ps
```

## 📝 Logs

```bash
# PostgreSQL
docker compose logs postgres

# pgAdmin
docker compose logs pgadmin
```

## 🛑 Parar o Ambiente

```bash
docker compose down
```

## 💾 Remover Dados

```bash
docker compose down -v
```

## 🔧 Acessar PostgreSQL via Terminal

```bash
docker exec -it postgres_db psql -U admin -d testdb
```

## 📁 Estrutura

- `docker-compose.yml` - Configuração dos serviços
- `EVIDENCIAS.html` - Documentação com evidências
- `test-environment.sh` - Script de teste
- `README.md` - Este arquivo

## ✅ Verificado

✓ PostgreSQL 16-alpine rodando  
✓ pgAdmin 4 rodando  
✓ Comunicação entre containers  
✓ Volume persistente configurado  
✓ Health checks funcionando  
