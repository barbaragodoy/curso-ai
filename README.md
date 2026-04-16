<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=curso-ai&fontSize=52&fontColor=fff&animation=twinkling&fontAlignY=36&desc=Intelig%C3%AAncia%20Artificial%20%26%20Ci%C3%AAncia%20de%20Dados&descAlignY=58&descSize=18" />

<br/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=6366F1&center=true&vCenter=true&random=false&width=620&lines=Algoritmos+e+Estrutura+de+Dados;Machine+Learning+%26+Deep+Learning;Banco+de+Dados+Nao-Relacional;Inteligencia+Artificial+Generativa;Big+Data+%26+Data+Science;Redes+Neurais+%26+Visao+Computacional)](https://git.io/typing-svg)

<br/>

![GitHub last commit](https://img.shields.io/github/last-commit/barbaragodoy/curso-ai?style=flat-square&color=6366f1)
![GitHub repo size](https://img.shields.io/github/repo-size/barbaragodoy/curso-ai?style=flat-square&color=22c55e)
![GitHub stars](https://img.shields.io/github/stars/barbaragodoy/curso-ai?style=flat-square&color=f59e0b)

</div>

---

## 👩‍💻 Sobre este repositório

Repositório com exercícios, projetos e atividades práticas desenvolvidos ao longo do curso de **Inteligência Artificial e Ciência de Dados**. Cada módulo representa uma disciplina com seus respectivos conteúdos e implementações.

<div align="center">
<img src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="480" alt="coding gif"/>
</div>

---

## 🗂️ Módulos

<div align="center">

| Módulo | Tópicos |
|--------|---------|
| 🧮 [Algoritmos](#-algoritmos) | Busca binária, ordenação |
| 🤖 [Aprendizagem de Máquina – Supervisionada](#-aprendizagem-de-máquina--supervisionada) | Classificação, regressão |
| 🔍 [Aprendizagem de Máquina – Não Supervisionada](#-aprendizagem-de-máquina--não-supervisionada) | Clustering, K-Means |
| 🍃 [Banco de Dados Não-Relacional](#-banco-de-dados-não-relacional) | MongoDB, Redis, PostgreSQL, ETL |
| 📊 [BI](#-bi) | KPIs, Business Intelligence |
| 🌐 [Big Data e Data Science](#-big-data-e-data-science) | Pandas, DataFrames |
| ⚡ [Computação Paralela](#-computação-paralela) | Multiprocessing |
| 🏗️ [Estrutura de Dados](#-estrutura-de-dados) | Ordenação, busca, pilhas |
| 🧠 [Inteligência Artificial](#-inteligência-artificial) | Agente de busca |
| ✨ [Inteligência Artificial Generativa](#-inteligência-artificial-generativa) | Geração de texto |
| 🐍 [Laboratório de Programação em Python](#-laboratório-de-programação-em-python) | Fundamentos Python |
| 📝 [Processamento de Linguagem Natural](#-processamento-de-linguagem-natural) | Tokenização, NLP |
| 🕸️ [Redes Neurais](#-redes-neurais) | Perceptron |
| ☁️ [Sistemas Distribuídos e Computação em Nuvem](#-sistemas-distribuídos-e-computação-em-nuvem) | APIs, Cloud |
| 👁️ [Visão Computacional](#-visão-computacional) | Processamento de imagem |

</div>

---

## 🧮 Algoritmos

Exercícios de busca binária e algoritmos fundamentais de ordenação e complexidade computacional.

---

## 🤖 Aprendizagem de Máquina – Supervisionada

<img align="right" src="https://media.giphy.com/media/LaVp0AyqR5bGsC5Cbm/giphy.gif" width="220"/>

Implementações práticas de algoritmos supervisionados:

- Classificação e regressão
- Métricas de avaliação de modelos
- Treinamento, validação e teste

<br clear="right"/>

---

## 🔍 Aprendizagem de Máquina – Não Supervisionada

Clustering e descoberta de padrões com K-Means e técnicas de aprendizado não supervisionado.

---

## 🍃 Banco de Dados Não-Relacional

<img align="right" src="https://media.giphy.com/media/KAq5w47R9rmTuxXbMM/giphy.gif" width="220"/>

Módulo completo sobre bancos de dados NoSQL:

| Projeto | Descrição |
|---------|-----------|
| `Introducao-Bancos-de-Dados-Nao-Relacionais` | Conceitos fundamentais NoSQL |
| `MongoDB-Pt-1` / `MongoDB-Pt-2` | Operações e consultas MongoDB |
| `Conexao-Configuraçao-Import-de-Dados-MongoDB-Atlas-Nuvem` | MongoDB Atlas na nuvem |
| `Aplicacão-Python-Docker` | Aplicação containerizada |
| `REDIS-Pt1/2/3` | Redis CLI, Python e imagens |
| `PostgreSQL-pgAdmin-Docker` | PostgreSQL com pgAdmin |
| ⭐ [`N1_ETL_NOSQL`](./Banco%20de%20Dados%20N%C3%A3o-Relacional/N1_ETL_NOSQL) | **Projeto N1 — Pipeline ETL completa** |

<br clear="right"/>

### ⭐ Projeto N1 — ETL BD Produção Artística

<div align="center">
<img src="https://media.giphy.com/media/fwbZnTftCXVocKzfxR/giphy.gif" width="380" alt="ETL pipeline"/>
</div>

Pipeline ETL completa para o dataset **BD_Producao_Artistica** com extração de JSONL, relatório de qualidade, transformação, carga em camadas RAW/CLEAN, enriquecimento de documentos e comparação relacional MongoDB vs PostgreSQL.

**Stack:**

[![My Skills](https://skillicons.dev/icons?i=python,fastapi,mongodb,postgres,docker,nginx)](https://skillicons.dev)

**Como rodar:**
```bash
cd "Banco de Dados Não-Relacional/N1_ETL_NOSQL"
cp .env.example .env
docker compose up --build
```
> Acesse em `http://localhost:3000`

---

## 📊 BI

KPIs e conceitos de Business Intelligence aplicados a cenários reais.

---

## 🌐 Big Data e Data Science

<img align="right" src="https://media.giphy.com/media/iIqmM5tTjmpOB9mpbn/giphy.gif" width="200"/>

Análise de dados com Pandas e DataFrames. Inclui notebook Jupyter com análise de salários de professores e manipulação de grandes volumes de dados.

<br clear="right"/>

---

## ⚡ Computação Paralela

Exercícios com `multiprocessing` em Python para processamento paralelo e concorrente.

---

## 🏗️ Estrutura de Dados

Implementações de algoritmos clássicos:
- **Ordenação:** Bubble Sort, Selection Sort
- **Busca:** Busca sequencial e binária
- **Estruturas:** Pilhas com push/pop

---

## 🧠 Inteligência Artificial

<img align="right" src="https://media.giphy.com/media/f3iwJFOVOwuy7K6FFw/giphy.gif" width="200"/>

Implementação de agentes inteligentes de busca, cobrindo estratégias de busca informada e não informada em espaços de estados.

<br clear="right"/>

---

## ✨ Inteligência Artificial Generativa

Exercícios de geração de texto simulada, explorando os fundamentos dos modelos generativos modernos.

---

## 🐍 Laboratório de Programação em Python

Listas de exercícios progressivos cobrindo os fundamentos da linguagem:

`Introdução` → `Estruturas Sequenciais` → `Condicionais` → `Repetições` → `Vetores`

---

## 📝 Processamento de Linguagem Natural

Tokenização e análise de texto, fundamentos de NLP para processamento e compreensão de linguagem humana.

---

## 🕸️ Redes Neurais

<img align="right" src="https://media.giphy.com/media/XH9LZPdFJNlTRSqTMJ/giphy.gif" width="200"/>

Implementação do Perceptron simples — bloco fundamental das redes neurais artificiais.

<br clear="right"/>

---

## ☁️ Sistemas Distribuídos e Computação em Nuvem

Exercícios de requisição a APIs externas, fundamentos de sistemas distribuídos e serviços em nuvem.

---

## 👁️ Visão Computacional

Exercícios de processamento de imagem, operações sobre pixels, filtros e análise visual.

---

## 🛠️ Tecnologias

<div align="center">

[![My Skills](https://skillicons.dev/icons?i=python,fastapi,mongodb,postgres,redis,docker,nginx,jupyter,git,github&perline=5)](https://skillicons.dev)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" />

**MIT © Barbara Godoy**

</div>
