"""
MongoDB Atlas Operations - Inserção de Dados e Queries
Conecta ao MongoDB Atlas e realiza operações de CRUD, agregação e indexação
"""

import pandas as pd
import pymongo
import urllib.parse
from datetime import datetime
import json


class MongoDBOperations:
    def __init__(self, username, password, cluster_uri):
        """
        Inicializa a conexão com MongoDB Atlas
        
        Args:
            username: Usuário do MongoDB Atlas
            password: Senha do MongoDB Atlas
            cluster_uri: URI do cluster (ex: cluster0.5kdvicj.mongodb.net)
        """
        self.username = username
        self.password = urllib.parse.quote_plus(password)
        self.cluster_uri = cluster_uri
        self.mongo_uri = f"mongodb+srv://{self.username}:{self.password}@{self.cluster_uri}/?retryWrites=true&w=majority"
        self.client = None
        self.db = None
        self.collection = None
        self.log = []
        
    def connect(self, database_name, collection_name):
        """Conecta ao MongoDB Atlas e acessa a coleção específica"""
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            # Testa a conexão
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
            self._log(f"✓ Conectado ao MongoDB Atlas - Banco: {database_name}, Coleção: {collection_name}")
            return True
        except Exception as e:
            self._log(f"✗ Erro na conexão: {str(e)}")
            return False
    
    def insert_data_from_csv(self, csv_path):
        """
        Lê dados do CSV e insere no MongoDB
        
        Args:
            csv_path: Caminho do arquivo CSV
        """
        try:
            df = pd.read_csv(csv_path)
            dados = df.to_dict(orient='records')
            
            # Remove a coluna de índice se existir
            for doc in dados:
                if 'Unnamed: 0' in doc:
                    del doc['Unnamed: 0']
            
            result = self.collection.insert_many(dados)
            self._log(f"✓ {len(result.inserted_ids)} documentos inseridos com sucesso")
            return True
        except Exception as e:
            self._log(f"✗ Erro ao inserir dados: {str(e)}")
            return False
    
    def query_by_genre(self, genre):
        """Busca filmes por gênero"""
        try:
            results = list(self.collection.find({"Genre": {"$regex": genre, "$options": "i"}}, {"_id": 0}))
            self._log(f"✓ Query por gênero '{genre}': {len(results)} resultados encontrados")
            return results
        except Exception as e:
            self._log(f"✗ Erro na query por gênero: {str(e)}")
            return []
    
    def query_by_rating(self, min_rate):
        """Busca filmes com nota mínima"""
        try:
            results = list(self.collection.find({"Rate": {"$gte": min_rate}}, {"_id": 0, "Title": 1, "Rate": 1}).sort("Rate", -1).limit(10))
            self._log(f"✓ Query por nota >= {min_rate}: {len(results)} resultados")
            return results
        except Exception as e:
            self._log(f"✗ Erro na query por nota: {str(e)}")
            return []
    
    def query_by_certificate(self, certificate):
        """Busca filmes por classificação etária"""
        try:
            count = self.collection.count_documents({"Certificate": certificate})
            results = list(self.collection.find({"Certificate": certificate}, {"_id": 0, "Title": 1, "Certificate": 1}).limit(5))
            self._log(f"✓ Filmes com classificação '{certificate}': {count} encontrados")
            return results
        except Exception as e:
            self._log(f"✗ Erro na query por certificado: {str(e)}")
            return []
    
    def aggregation_avg_rating_by_certificate(self):
        """Agregação: Média de nota por classificação etária"""
        try:
            pipeline = [
                {
                    "$group": {
                        "_id": "$Certificate",
                        "average_rate": {"$avg": "$Rate"},
                        "count": {"$sum": 1}
                    }
                },
                {"$sort": {"average_rate": -1}}
            ]
            results = list(self.collection.aggregate(pipeline))
            self._log(f"✓ Agregação: Média de nota por certificado - {len(results)} grupos")
            return results
        except Exception as e:
            self._log(f"✗ Erro na agregação: {str(e)}")
            return []
    
    def aggregation_top_directors(self):
        """Agregação: Diretores com mais filmes"""
        try:
            pipeline = [
                {"$addFields": {"director": {"$arrayElemAt": [{"$split": ["$Cast", "|"]}, 0]}}},
                {
                    "$group": {
                        "_id": "$director",
                        "count": {"$sum": 1},
                        "avg_rate": {"$avg": "$Rate"}
                    }
                },
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            results = list(self.collection.aggregate(pipeline))
            self._log(f"✓ Agregação: Top 10 diretores - {len(results)} resultados")
            return results
        except Exception as e:
            self._log(f"✗ Erro na agregação de diretores: {str(e)}")
            return []
    
    def aggregation_genre_statistics(self):
        """Agregação: Estatísticas por gênero"""
        try:
            pipeline = [
                {"$unwind": "$Genre"},
                {
                    "$group": {
                        "_id": "$Genre",
                        "count": {"$sum": 1},
                        "avg_rate": {"$avg": "$Rate"},
                        "max_rate": {"$max": "$Rate"},
                        "min_rate": {"$min": "$Rate"}
                    }
                },
                {"$sort": {"avg_rate": -1}}
            ]
            results = list(self.collection.aggregate(pipeline))
            self._log(f"✓ Agregação: Estatísticas por gênero - {len(results)} gêneros")
            return results
        except Exception as e:
            self._log(f"✗ Erro na agregação de gêneros: {str(e)}")
            return []
    
    def create_index_title(self):
        """Cria índice no campo Title"""
        try:
            self.collection.create_index("Title")
            self._log("✓ Índice criado: Title")
            return True
        except Exception as e:
            self._log(f"✗ Erro ao criar índice Title: {str(e)}")
            return False
    
    def create_index_rate(self):
        """Cria índice no campo Rate"""
        try:
            self.collection.create_index("Rate")
            self._log("✓ Índice criado: Rate")
            return True
        except Exception as e:
            self._log(f"✗ Erro ao criar índice Rate: {str(e)}")
            return False
    
    def create_index_certificate(self):
        """Cria índice no campo Certificate"""
        try:
            self.collection.create_index("Certificate")
            self._log("✓ Índice criado: Certificate")
            return True
        except Exception as e:
            self._log(f"✗ Erro ao criar índice Certificate: {str(e)}")
            return False
    
    def create_compound_index(self):
        """Cria índice composto em Genre e Rate"""
        try:
            self.collection.create_index([("Genre", 1), ("Rate", -1)])
            self._log("✓ Índice composto criado: Genre + Rate (descendente)")
            return True
        except Exception as e:
            self._log(f"✗ Erro ao criar índice composto: {str(e)}")
            return False
    
    def list_indexes(self):
        """Lista todos os índices da coleção"""
        try:
            indexes = self.collection.list_indexes()
            self._log(f"✓ Índices listados: {len(list(indexes))} índices encontrados")
            return list(self.collection.list_indexes())
        except Exception as e:
            self._log(f"✗ Erro ao listar índices: {str(e)}")
            return []
    
    def _log(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log.append(log_entry)
        print(log_entry)
    
    def save_log(self, filename="mongodb_operations_log.txt"):
        """Salva o log em arquivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.log))
            print(f"\n✓ Log salvo em: {filename}")
        except Exception as e:
            print(f"✗ Erro ao salvar log: {str(e)}")
    
    def disconnect(self):
        """Desconecta do MongoDB"""
        if self.client:
            self.client.close()
            self._log("✓ Desconectado do MongoDB Atlas")


def main():
    """Função principal para executar todas as operações"""
    
    # Configurações
    USERNAME = "admin"
    PASSWORD = "admin"
    CLUSTER_URI = "cluster0.5kdvicj.mongodb.net"
    DATABASE_NAME = "imdb"
    COLLECTION_NAME = "movies"
    CSV_PATH = "IMDB top 1000.csv"
    
    # Inicializa operações
    mongo_ops = MongoDBOperations(USERNAME, PASSWORD, CLUSTER_URI)
    
    print("=" * 60)
    print("MongoDB Atlas - Operações CRUD, Agregação e Indexação")
    print("=" * 60)
    
    # Conecta
    if not mongo_ops.connect(DATABASE_NAME, COLLECTION_NAME):
        print("Falha na conexão. Abortando...")
        return
    
    # Insere dados
    print("\n--- Inserção de Dados ---")
    mongo_ops.insert_data_from_csv(CSV_PATH)
    
    # Queries
    print("\n--- Queries ---")
    
    print("\n1. Filmes de Drama:")
    dramas = mongo_ops.query_by_genre("Drama")
    for i, film in enumerate(dramas[:3], 1):
        print(f"   {i}. {film.get('Title')} - {film.get('Rate')}")
    
    print("\n2. Filmes com nota >= 8.8:")
    top_rated = mongo_ops.query_by_rating(8.8)
    for i, film in enumerate(top_rated[:3], 1):
        print(f"   {i}. {film.get('Title')} - {film.get('Rate')}")
    
    print("\n3. Filmes com classificação R:")
    rated_r = mongo_ops.query_by_certificate("R")
    for i, film in enumerate(rated_r[:3], 1):
        print(f"   {i}. {film.get('Title')} - {film.get('Certificate')}")
    
    # Agregações
    print("\n--- Agregações ---")
    
    print("\n1. Média de nota por classificação etária:")
    avg_by_cert = mongo_ops.aggregation_avg_rating_by_certificate()
    for result in avg_by_cert[:5]:
        print(f"   {result['_id']}: média {result['average_rate']:.2f} ({result['count']} filmes)")
    
    print("\n2. Estatísticas por gênero:")
    genre_stats = mongo_ops.aggregation_genre_statistics()
    for result in genre_stats[:5]:
        print(f"   {result['_id']}: {result['count']} filmes, "
              f"média {result['avg_rate']:.2f}, "
              f"min {result['min_rate']}, max {result['max_rate']}")
    
    # Índices
    print("\n--- Criação de Índices ---")
    mongo_ops.create_index_title()
    mongo_ops.create_index_rate()
    mongo_ops.create_index_certificate()
    mongo_ops.create_compound_index()
    
    print("\n--- Índices Criados ---")
    for index in mongo_ops.list_indexes():
        print(f"   Índice: {index.get('name')} - {index.get('key')}")
    
    # Salva log
    mongo_ops.save_log()
    
    # Desconecta
    mongo_ops.disconnect()
    
    print("\n" + "=" * 60)
    print("Operações concluídas!")
    print("=" * 60)


if __name__ == "__main__":
    main()
