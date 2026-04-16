# Repositório de Estudos — Curso IA & Dados

Repositório com exercícios, projetos e atividades práticas desenvolvidos ao longo do curso de Inteligência Artificial e Ciência de Dados.

---

## Estrutura

| Módulo | Conteúdo |
|--------|----------|
| [Algoritmos](#algoritmos) | Busca binária, ordenação |
| [Aprendizagem de Máquina – Supervisionada](#aprendizagem-de-máquina--supervisionada) | Classificação, regressão |
| [Aprendizagem de Máquina – Não Supervisionada](#aprendizagem-de-máquina--não-supervisionada) | Clustering, K-Means |
| [Banco de Dados Não-Relacional](#banco-de-dados-não-relacional) | MongoDB, Redis, PostgreSQL, ETL NoSQL |
| [BI](#bi) | KPIs, Business Intelligence |
| [Big Data e Data Science](#big-data-e-data-science) | Pandas, DataFrames, análise de dados |
| [Computação Paralela](#computação-paralela) | Multiprocessing |
| [Estrutura de Dados](#estrutura-de-dados) | Ordenação, busca, pilhas |
| [Inteligência Artificial](#inteligência-artificial) | Agente de busca |
| [Inteligência Artificial Generativa](#inteligência-artificial-generativa) | Geração de texto |
| [Laboratório de Programação em Python](#laboratório-de-programação-em-python) | Listas, condicionais, vetores |
| [Processamento de Linguagem Natural](#processamento-de-linguagem-natural) | Tokenização, análise textual |
| [Redes Neurais](#redes-neurais) | Perceptron |
| [Sistemas Distribuídos e Computação em Nuvem](#sistemas-distribuídos-e-computação-em-nuvem) | APIs, requisições HTTP |
| [Visão Computacional](#visão-computacional) | Processamento de imagem |

---

## Módulos

### Algoritmos
Exercícios de busca binária e algoritmos fundamentais.

### Aprendizagem de Máquina – Supervisionada
Exercícios práticos de classificação e regressão.

### Aprendizagem de Máquina – Não Supervisionada
Implementação de clustering com K-Means.

### Banco de Dados Não-Relacional
Módulo completo sobre bancos NoSQL com MongoDB, Redis e PostgreSQL.

| Projeto | Descrição |
|---------|-----------|
| `Introducao-Bancos-de-Dados-Nao-Relacionais` | Conceitos fundamentais de NoSQL |
| `MongoDB-Pt-1` / `MongoDB-Pt-2` | Operações e consultas no MongoDB |
| `Conexao-Configuraçao-Import-de-Dados-MongoDB-Atlas-Nuvem` | Integração com MongoDB Atlas |
| `Aplicacão-Python-Docker` | Aplicação Python containerizada |
| `REDIS-Pt1` / `REDIS-Pt-2` / `REDIS-Pt-3` | Redis CLI, Python e armazenamento de imagens |
| `PostgreSQL-pgAdmin-Docker` | PostgreSQL com pgAdmin via Docker |
| [`N1_ETL_NOSQL`](./Banco%20de%20Dados%20N%C3%A3o-Relacional/N1_ETL_NOSQL) | **Projeto N1 — Pipeline ETL completa com MongoDB** |

#### N1 — ETL BD Produção Artística
Pipeline ETL completa para o dataset BD_Producao_Artistica com FastAPI, MongoDB, PostgreSQL e frontend web.

**Stack:** Python · FastAPI · MongoDB 7 · PostgreSQL 16 · Docker · Nginx

**Como rodar:**
```bash
cd "Banco de Dados Não-Relacional/N1_ETL_NOSQL"
cp .env.example .env
docker compose up --build
```
Acesse em `http://localhost:3000`

### BI
KPIs e conceitos de Business Intelligence.

### Big Data e Data Science
Análise de dados com Pandas e DataFrames. Inclui notebook Jupyter com análise de salários de professores.

### Computação Paralela
Exercícios com `multiprocessing` em Python.

### Estrutura de Dados
Algoritmos de ordenação (Bubble Sort, Selection Sort), busca sequencial e estruturas como pilhas.

### Inteligência Artificial
Implementação de agente de busca.

### Inteligência Artificial Generativa
Exercício de geração de texto simulada.

### Laboratório de Programação em Python
Listas de exercícios progressivos: introdução, estruturas sequenciais, condicionais, repetições e vetores.

### Processamento de Linguagem Natural
Tokenização e análise de texto.

### Redes Neurais
Implementação do Perceptron simples.

### Sistemas Distribuídos e Computação em Nuvem
Exercícios de requisição a APIs externas.

### Visão Computacional
Exercícios de processamento de imagem.

---

## Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

---

## Licença

MIT © Barbara Godoy
