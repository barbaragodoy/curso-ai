#!/usr/bin/env python3
"""
Gerador Automático de Referências (ABNT/APA) - Web
Aplicação Flask para gerar citações formatadas.
"""

from flask import Flask, render_template, request, jsonify, send_file
from reference_generator import ReferenceGenerator
import json
import io
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Instância global do gerador
generator = ReferenceGenerator()


@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html')


@app.route('/api/add-book', methods=['POST'])
def add_book():
    """API para adicionar um livro."""
    try:
        data = request.json
        ref = generator.add_book(
            author=data.get('author', ''),
            title=data.get('title', ''),
            year=int(data.get('year', datetime.now().year)),
            publisher=data.get('publisher', ''),
            edition=data.get('edition', '1ª'),
            place=data.get('place', 'São Paulo')
        )
        return jsonify({
            'status': 'success',
            'message': f'Livro "{data.get("title")}" adicionado com sucesso!',
            'abnt': generator.format_abnt(ref),
            'apa': generator.format_apa(ref)
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/add-website', methods=['POST'])
def add_website():
    """API para adicionar um website."""
    try:
        data = request.json
        ref = generator.add_website(
            url=data.get('url', ''),
            title=data.get('title', ''),
            author=data.get('author', 'Autor desconhecido'),
            access_date=data.get('access_date', datetime.now().strftime('%d de %B de %Y'))
        )
        return jsonify({
            'status': 'success',
            'message': f'Website "{data.get("title")}" adicionado com sucesso!',
            'abnt': generator.format_abnt(ref),
            'apa': generator.format_apa(ref)
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/add-article', methods=['POST'])
def add_article():
    """API para adicionar um artigo científico."""
    try:
        data = request.json
        ref = generator.add_article(
            author=data.get('author', ''),
            title=data.get('title', ''),
            journal=data.get('journal', ''),
            year=int(data.get('year', datetime.now().year)),
            volume=data.get('volume', '1'),
            issue=data.get('issue', '1'),
            pages=data.get('pages', '1-10'),
            doi=data.get('doi', None)
        )
        return jsonify({
            'status': 'success',
            'message': f'Artigo "{data.get("title")}" adicionado com sucesso!',
            'abnt': generator.format_abnt(ref),
            'apa': generator.format_apa(ref)
        }), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/references', methods=['GET'])
def get_references():
    """API para obter todas as referências."""
    format_type = request.args.get('format', 'abnt').lower()
    
    if format_type == 'abnt':
        references = generator.get_all_references_abnt()
    elif format_type == 'apa':
        references = generator.get_all_references_apa()
    else:
        return jsonify({'status': 'error', 'message': 'Formato inválido'}), 400
    
    return jsonify({
        'status': 'success',
        'format': format_type.upper(),
        'count': len(references),
        'references': references
    }), 200


@app.route('/api/export', methods=['GET'])
def export_references():
    """API para exportar referências."""
    format_type = request.args.get('format', 'json').lower()
    
    if format_type == 'json':
        json_data = generator.to_json('abnt')
        return send_file(
            io.BytesIO(json_data.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'referencias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
    
    elif format_type == 'txt':
        generator.save_to_file('/tmp/referencias_abnt.txt', 'abnt')
        with open('/tmp/referencias_abnt.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'referencias_abnt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
    
    return jsonify({'status': 'error', 'message': 'Formato inválido'}), 400


@app.route('/api/clear', methods=['POST'])
def clear_references():
    """API para limpar todas as referências."""
    global generator
    generator = ReferenceGenerator()
    return jsonify({
        'status': 'success',
        'message': 'Todas as referências foram removidas!'
    }), 200


@app.route('/api/count', methods=['GET'])
def count_references():
    """API para obter contagem de referências."""
    return jsonify({
        'status': 'success',
        'count': len(generator.references),
        'references': generator.references
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
