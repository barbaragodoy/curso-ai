# Gerador Automático de Referências (ABNT/APA) - Docker

Uma aplicação Python que gera citações formatadas corretamente nos formatos **ABNT** e **APA**. Suporta referências de livros, websites e artigos científicos.

## Arquivos do Projeto

- **reference_generator.py** - Código principal da aplicação
- **Dockerfile** - Imagem Docker multi-stage otimizada (Python 3.11-slim)
- **docker-compose.yml** - Orquestração do container
- **requirements.txt** - Dependências Python
- **.dockerignore** - Arquivos ignorados no build
- **outputs/** - Diretório para saída de referências

## Funcionalidades

✅ Adicionar livros, websites e artigos  
✅ Formatar automaticamente em ABNT  
✅ Formatar automaticamente em APA  
✅ Exportar para arquivos de texto  
✅ Exportar para JSON  

## Instalação e Execução

### Com Docker Compose (Recomendado)

```bash
docker compose up
```

A aplicação irá:
1. Construir a imagem automaticamente
2. Executar a geração de referências
3. Salvar os arquivos em `outputs/`

### Com Docker Directly

```bash
docker build -t reference-generator .
docker run -v ./outputs:/app/outputs reference-generator
```

## Saída Esperada

A aplicação gera 3 arquivos em `outputs/`:

- **referencias_abnt.txt** - Referências formatadas em ABNT
- **referencias_apa.txt** - Referências formatadas em APA
- **referencias.json** - Dados estruturados em JSON

## Exemplo de Uso Programático

```python
from reference_generator import ReferenceGenerator

generator = ReferenceGenerator()

# Adicionar um livro
generator.add_book(
    author='Paulo Coelho',
    title='O Alquimista',
    year=1988,
    publisher='HarperOne',
    edition='2ª',
    place='Nova York'
)

# Adicionar um website
generator.add_website(
    url='https://www.python.org',
    title='Python Official Website',
    author='Python Software Foundation'
)

# Adicionar um artigo científico
generator.add_article(
    author='Silva, João; Santos, Maria',
    title='Análise de Containerização',
    journal='Revista de Tecnologia',
    year=2023,
    volume='5',
    issue='2',
    pages='45-62',
    doi='10.1234/rt.2023.5.2'
)

# Obter referências
refs_abnt = generator.get_all_references_abnt()
refs_apa = generator.get_all_references_apa()

# Salvar em arquivos
generator.save_to_file('referencias_abnt.txt', 'abnt')
generator.save_to_file('referencias_apa.txt', 'apa')

# Exportar para JSON
json_data = generator.to_json('abnt')
```

## Estrutura Docker

### Dockerfile Multi-Stage

- **Stage 1 (builder)**: Python 3.11-slim + instalação de dependências
- **Stage 2 (final)**: Imagem otimizada contendo apenas o necessário

Benefícios:
- Imagem final compacta (~150MB)
- Sem ferramentas de build desnecessárias
- Melhor segurança
- Cache eficiente

### Volumes

- `./outputs:/app/outputs` - Diretório onde os arquivos gerados são salvos

## Requisitos

- Docker 20.10+
- Docker Compose 2.0+

## Exemplo de Saída

### Formato ABNT
```
MACHADO DE ASSIS. Dom Casmurro. 1ª ed. Rio de Janeiro: Editora Garnier, 1899.
PYTHON SOFTWARE FOUNDATION. Python Official Website. Disponível em: https://www.python.org. Acesso em: 11 de April de 2026.
```

### Formato APA
```
Machado de Assis (1899). Dom Casmurro. Rio de Janeiro: Editora Garnier.
Python Software Foundation. Python Official Website. Retrieved from https://www.python.org (Accessed: 11 de April de 2026)
```

## Desenvolvimento

Para modificar a aplicação:

1. Edite `reference_generator.py`
2. Reconstrua a imagem: `docker compose build --no-cache`
3. Execute: `docker compose up`
