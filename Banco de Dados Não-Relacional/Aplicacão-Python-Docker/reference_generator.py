#!/usr/bin/env python3
"""
Gerador Automático de Referências (ABNT/APA)
Converte URLs e dados de livros em citações formatadas corretamente.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse


class ReferenceGenerator:
    """Classe para gerar referências em formatos ABNT e APA."""

    def __init__(self):
        self.references = []

    def add_book(self, **kwargs) -> Dict:
        """
        Adiciona um livro e gera citações.
        
        Args:
            author: Nome do(s) autor(es)
            title: Título do livro
            year: Ano de publicação
            publisher: Nome da editora
            edition: Edição (opcional)
            place: Local de publicação (opcional)
        """
        ref = {
            'type': 'book',
            'author': kwargs.get('author', 'Desconhecido'),
            'title': kwargs.get('title', 'Sem título'),
            'year': kwargs.get('year', datetime.now().year),
            'publisher': kwargs.get('publisher', ''),
            'edition': kwargs.get('edition', '1ª'),
            'place': kwargs.get('place', 'São Paulo'),
        }
        self.references.append(ref)
        return ref

    def add_website(self, **kwargs) -> Dict:
        """
        Adiciona um site/URL e gera citações.
        
        Args:
            url: URL do site
            title: Título da página
            author: Autor/responsável (opcional)
            access_date: Data de acesso (formato YYYY-MM-DD, opcional)
        """
        url = kwargs.get('url', '')
        ref = {
            'type': 'website',
            'url': url,
            'title': kwargs.get('title', self._extract_title_from_url(url)),
            'author': kwargs.get('author', 'Autor desconhecido'),
            'access_date': kwargs.get('access_date', datetime.now().strftime('%d de %B de %Y')),
            'domain': urlparse(url).netloc,
        }
        self.references.append(ref)
        return ref

    def add_article(self, **kwargs) -> Dict:
        """
        Adiciona um artigo científico e gera citações.
        
        Args:
            author: Nome do(s) autor(es)
            title: Título do artigo
            journal: Nome do periódico
            year: Ano de publicação
            volume: Volume
            issue: Número/Edição
            pages: Páginas (formato: 10-25)
            doi: DOI (opcional)
        """
        ref = {
            'type': 'article',
            'author': kwargs.get('author', 'Desconhecido'),
            'title': kwargs.get('title', 'Sem título'),
            'journal': kwargs.get('journal', 'Periódico desconhecido'),
            'year': kwargs.get('year', datetime.now().year),
            'volume': kwargs.get('volume', '1'),
            'issue': kwargs.get('issue', '1'),
            'pages': kwargs.get('pages', '1-10'),
            'doi': kwargs.get('doi', None),
        }
        self.references.append(ref)
        return ref

    def format_abnt(self, ref: Dict) -> str:
        """Formata referência em ABNT."""
        ref_type = ref.get('type')
        
        if ref_type == 'book':
            return self._format_book_abnt(ref)
        elif ref_type == 'website':
            return self._format_website_abnt(ref)
        elif ref_type == 'article':
            return self._format_article_abnt(ref)
        
        return "Tipo de referência não suportado"

    def format_apa(self, ref: Dict) -> str:
        """Formata referência em APA."""
        ref_type = ref.get('type')
        
        if ref_type == 'book':
            return self._format_book_apa(ref)
        elif ref_type == 'website':
            return self._format_website_apa(ref)
        elif ref_type == 'article':
            return self._format_article_apa(ref)
        
        return "Tipo de referência não suportado"

    def _format_book_abnt(self, ref: Dict) -> str:
        """Formata livro em ABNT."""
        author = ref['author'].upper()
        title = ref['title']
        edition = ref['edition']
        place = ref['place']
        publisher = ref['publisher']
        year = ref['year']
        
        return f"{author}. {title}. {edition} ed. {place}: {publisher}, {year}."

    def _format_book_apa(self, ref: Dict) -> str:
        """Formata livro em APA."""
        author = ref['author']
        title = ref['title']
        place = ref['place']
        publisher = ref['publisher']
        year = ref['year']
        
        return f"{author} ({year}). {title}. {place}: {publisher}."

    def _format_website_abnt(self, ref: Dict) -> str:
        """Formata website em ABNT."""
        author = ref['author'].upper()
        title = ref['title']
        url = ref['url']
        access_date = ref['access_date']
        
        return f"{author}. {title}. Disponível em: {url}. Acesso em: {access_date}."

    def _format_website_apa(self, ref: Dict) -> str:
        """Formata website em APA."""
        author = ref['author']
        title = ref['title']
        url = ref['url']
        access_date = ref['access_date']
        
        return f"{author}. {title}. Retrieved from {url} (Accessed: {access_date})"

    def _format_article_abnt(self, ref: Dict) -> str:
        """Formata artigo em ABNT."""
        author = ref['author'].upper()
        title = ref['title']
        journal = ref['journal']
        year = ref['year']
        volume = ref['volume']
        issue = ref['issue']
        pages = ref['pages']
        
        citation = f"{author}. {title}. {journal}, v. {volume}, n. {issue}, p. {pages}, {year}."
        
        if ref['doi']:
            citation += f" DOI: {ref['doi']}"
        
        return citation

    def _format_article_apa(self, ref: Dict) -> str:
        """Formata artigo em APA."""
        author = ref['author']
        title = ref['title']
        journal = ref['journal']
        year = ref['year']
        volume = ref['volume']
        issue = ref['issue']
        pages = ref['pages']
        
        citation = f"{author} ({year}). {title}. {journal}, {volume}({issue}), {pages}."
        
        if ref['doi']:
            citation += f" https://doi.org/{ref['doi']}"
        
        return citation

    def _extract_title_from_url(self, url: str) -> str:
        """Extrai um título legível da URL."""
        domain = urlparse(url).netloc.replace('www.', '')
        return domain.split('.')[0].title()

    def get_all_references_abnt(self) -> List[str]:
        """Retorna todas as referências formatadas em ABNT."""
        return [self.format_abnt(ref) for ref in self.references]

    def get_all_references_apa(self) -> List[str]:
        """Retorna todas as referências formatadas em APA."""
        return [self.format_apa(ref) for ref in self.references]

    def save_to_file(self, filename: str, format_type: str = 'abnt') -> None:
        """Salva referências em arquivo de texto."""
        if format_type.lower() == 'abnt':
            references = self.get_all_references_abnt()
        else:
            references = self.get_all_references_apa()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Referências - Formato {format_type.upper()}\n")
            f.write("=" * 50 + "\n\n")
            for idx, ref in enumerate(references, 1):
                f.write(f"{idx}. {ref}\n\n")

    def to_json(self, format_type: str = 'abnt') -> str:
        """Retorna referências em formato JSON."""
        if format_type.lower() == 'abnt':
            formatted_refs = self.get_all_references_abnt()
        else:
            formatted_refs = self.get_all_references_apa()
        
        data = {
            'format': format_type.upper(),
            'references': formatted_refs,
            'count': len(formatted_refs),
            'generated_at': datetime.now().isoformat(),
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    """Função principal - demonstração da aplicação."""
    print("=" * 60)
    print("GERADOR AUTOMÁTICO DE REFERÊNCIAS (ABNT/APA)")
    print("=" * 60)
    print()

    generator = ReferenceGenerator()

    # Exemplo 1: Adicionando um livro
    print("📚 Adicionando um livro...")
    generator.add_book(
        author='Machado de Assis',
        title='Dom Casmurro',
        year=1899,
        publisher='Editora Garnier',
        edition='1ª',
        place='Rio de Janeiro'
    )
    print()

    # Exemplo 2: Adicionando um website
    print("🌐 Adicionando um website...")
    generator.add_website(
        url='https://www.python.org',
        title='Python Official Website',
        author='Python Software Foundation',
        access_date=datetime.now().strftime('%d de %B de %Y')
    )
    print()

    # Exemplo 3: Adicionando um artigo científico
    print("📄 Adicionando um artigo científico...")
    generator.add_article(
        author='Silva, João; Santos, Maria',
        title='Análise de Containerização em Aplicações Modernas',
        journal='Revista de Tecnologia',
        year=2023,
        volume='5',
        issue='2',
        pages='45-62',
        doi='10.1234/rt.2023.5.2'
    )
    print()

    # Exemplo 4: Adicionando mais um livro
    print("📚 Adicionando outro livro...")
    generator.add_book(
        author='Paulo Coelho',
        title='O Alquimista',
        year=1988,
        publisher='HarperOne',
        edition='2ª',
        place='Nova York'
    )
    print()

    # Exibindo referências em ABNT
    print("=" * 60)
    print("REFERÊNCIAS - FORMATO ABNT")
    print("=" * 60)
    for idx, ref in enumerate(generator.get_all_references_abnt(), 1):
        print(f"{idx}. {ref}")
    print()

    # Exibindo referências em APA
    print("=" * 60)
    print("REFERÊNCIAS - FORMATO APA")
    print("=" * 60)
    for idx, ref in enumerate(generator.get_all_references_apa(), 1):
        print(f"{idx}. {ref}")
    print()

    # Salvando em arquivos
    print("💾 Salvando referências em arquivos...")
    generator.save_to_file('/app/outputs/referencias_abnt.txt', 'abnt')
    generator.save_to_file('/app/outputs/referencias_apa.txt', 'apa')
    print("✅ Arquivos criados: /app/outputs/referencias_abnt.txt e /app/outputs/referencias_apa.txt")
    print()

    # Exportando para JSON
    print("📋 Exportando para JSON...")
    json_abnt = generator.to_json('abnt')
    json_apa = generator.to_json('apa')
    
    with open('/app/outputs/referencias.json', 'w', encoding='utf-8') as f:
        f.write(json_abnt)
    print("✅ Arquivo gerado: /app/outputs/referencias.json")
    print()

    print("=" * 60)
    print("✨ Aplicação executada com sucesso!")
    print("=" * 60)


if __name__ == '__main__':
    main()
