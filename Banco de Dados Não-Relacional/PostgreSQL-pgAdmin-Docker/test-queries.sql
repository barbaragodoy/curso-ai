-- Script de teste para PostgreSQL
-- Executar no pgAdmin Query Tool

-- 1. Verificar versão do PostgreSQL
SELECT version();

-- 2. Listar todas as bases de dados
SELECT datname FROM pg_database WHERE datistemplate = false;

-- 3. Criar tabela de exemplo
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Inserir dados de exemplo
INSERT INTO usuarios (nome, email) VALUES 
('João Silva', 'joao@example.com'),
('Maria Santos', 'maria@example.com'),
('Pedro Oliveira', 'pedro@example.com');

-- 5. Consultar dados
SELECT * FROM usuarios;

-- 6. Contar registros
SELECT COUNT(*) as total_usuarios FROM usuarios;

-- 7. Verificar informações da conexão
SHOW server_version;
SHOW database;
SHOW user;

-- 8. Listar todas as tabelas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- 9. Ver estrutura da tabela
\d usuarios

-- 10. Timestamp da última execução
SELECT NOW() as horario_atual;
