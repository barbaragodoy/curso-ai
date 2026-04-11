"""
MongoDB Atlas - Script de Teste Rápido
Valida a conexão e executa operações básicas
"""

import pymongo
import urllib.parse


def test_connection():
    """Testa conexão com MongoDB Atlas"""
    
    print("=" * 70)
    print("TESTE DE CONEXÃO - MongoDB Atlas")
    print("=" * 70)
    
    # Credenciais
    username = "admin"
    password = "admin"
    cluster_uri = "cluster0.5kdvicj.mongodb.net"
    
    # Monta URI
    password_encoded = urllib.parse.quote_plus(password)
    mongo_uri = f"mongodb+srv://{username}:{password_encoded}@{cluster_uri}/?retryWrites=true&w=majority"
    
    print(f"\n🔌 Conectando a: {cluster_uri}")
    print(f"👤 Usuário: {username}")
    
    try:
        # Conecta
        client = pymongo.MongoClient(mongo_uri)
        
        # Testa com ping
        client.admin.command('ping')
        print("✓ Conexão estabelecida com sucesso!")
        
        # Obtém informações do servidor
        server_info = client.server_info()
        print(f"✓ Versão do servidor: {server_info.get('version', 'N/A')}")
        
        # Lista bancos de dados
        print("\n📊 Bancos de dados disponíveis:")
        databases = client.list_database_names()
        for db_name in databases[:5]:  # Mostra apenas 5 primeiros
            print(f"   - {db_name}")
        
        # Acessa banco 'imdb' se existir
        if 'imdb' in databases:
            db = client['imdb']
            print(f"\n✓ Banco 'imdb' encontrado")
            
            # Lista coleções
            collections = db.list_collection_names()
            print(f"✓ Coleções no banco 'imdb':")
            for coll_name in collections:
                print(f"   - {coll_name}")
                
                # Se 'movies' existir, mostra estatísticas
                if coll_name == 'movies':
                    collection = db[coll_name]
                    count = collection.count_documents({})
                    print(f"     └─ {count} documentos")
                    
                    # Exemplo de documento
                    sample = collection.find_one({})
                    if sample:
                        print(f"\n📄 Exemplo de documento:")
                        print(f"   Title: {sample.get('Title', 'N/A')}")
                        print(f"   Rate: {sample.get('Rate', 'N/A')}")
                        print(f"   Genre: {sample.get('Genre', 'N/A')}")
                        print(f"   Certificate: {sample.get('Certificate', 'N/A')}")
        
        # Desconecta
        client.close()
        print("\n✓ Desconectado com sucesso")
        
        print("\n" + "=" * 70)
        print("✓ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n✗ Erro de conexão: {str(e)}")
        print("\nDicas de troubleshooting:")
        print("1. Verifique username e password")
        print("2. Verifique se o IP 149.78.206.47 está autorizado no MongoDB Atlas")
        print("3. Verifique se a URL do cluster está correta")
        print("4. Verifique conexão com internet")
        print("\n" + "=" * 70)
        return False


if __name__ == "__main__":
    test_connection()
