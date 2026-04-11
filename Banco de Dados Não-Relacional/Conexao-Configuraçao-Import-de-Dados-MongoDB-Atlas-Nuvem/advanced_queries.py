"""
MongoDB Atlas - Consultas Avançadas e Análise
Script com operações mais complexas e análises de dados
"""

import pymongo
import urllib.parse
from datetime import datetime


class AdvancedMongoDBOperations:
    def __init__(self, username, password, cluster_uri):
        self.username = username
        self.password = urllib.parse.quote_plus(password)
        self.cluster_uri = cluster_uri
        self.mongo_uri = f"mongodb+srv://{self.username}:{self.password}@{self.cluster_uri}/?retryWrites=true&w=majority"
        self.client = None
        self.db = None
        self.collection = None
        self.results_log = []
    
    def connect(self, database_name, collection_name):
        """Conecta ao MongoDB"""
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
            self.log(f"✓ Conectado: {database_name}.{collection_name}")
            return True
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return False
    
    def log(self, message):
        """Registra mensagem"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.results_log.append(entry)
        print(entry)
    
    # ===== CONSULTAS =====
    
    def query_movies_with_metascore(self, min_metascore=90):
        """Filmes com metascore mínimo"""
        try:
            results = list(self.collection.find(
                {"Metascore": {"$gte": min_metascore}},
                {"_id": 0, "Title": 1, "Rate": 1, "Metascore": 1}
            ).sort("Metascore", -1).limit(10))
            self.log(f"✓ {len(results)} filmes com Metascore >= {min_metascore}")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    def query_top_10_movies(self):
        """Top 10 filmes por nota"""
        try:
            results = list(self.collection.find(
                {},
                {"_id": 0, "Title": 1, "Rate": 1, "Year": 1}
            ).sort("Rate", -1).limit(10))
            self.log(f"✓ Top 10 filmes recuperados")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    def query_movies_by_year_range(self, start_year, end_year):
        """Filmes em um intervalo de anos"""
        try:
            results = list(self.collection.find(
                {"Year": {"$gte": start_year, "$lte": end_year}},
                {"_id": 0, "Title": 1, "Year": 1, "Rate": 1}
            ).sort("Year", -1))
            self.log(f"✓ {len(results)} filmes entre {start_year} e {end_year}")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    def query_movies_by_duration(self, min_duration, max_duration):
        """Filmes com duração específica"""
        try:
            results = list(self.collection.find(
                {"Duration": {"$regex": "\\d+", "$options": ""}},
                {"_id": 0, "Title": 1, "Duration": 1, "Rate": 1}
            ).limit(10))
            self.log(f"✓ Filmes com duração consultados")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    def query_text_search(self, search_term):
        """Busca por texto no título ou descrição"""
        try:
            results = list(self.collection.find(
                {"$or": [
                    {"Title": {"$regex": search_term, "$options": "i"}},
                    {"Description": {"$regex": search_term, "$options": "i"}}
                ]},
                {"_id": 0, "Title": 1, "Rate": 1}
            ).limit(5))
            self.log(f"✓ {len(results)} resultados para '{search_term}'")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    # ===== AGREGAÇÕES =====
    
    def aggregation_movies_by_certificate_and_genre(self):
        """Agregação: Filmes por certificado e gênero"""
        try:
            pipeline = [
                {"$unwind": "$Genre"},
                {
                    "$group": {
                        "_id": {
                            "certificate": "$Certificate",
                            "genre": "$Genre"
                        },
                        "count": {"$sum": 1},
                        "avg_rate": {"$avg": "$Rate"}
                    }
                },
                {"$sort": {"count": -1}},
                {"$limit": 15}
            ]
            results = list(self.collection.aggregate(pipeline))
            self.log(f"✓ Agregação: {len(results)} combinações cert/gênero")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    def aggregation_rating_distribution(self):
        """Agregação: Distribuição de notas"""
        try:
            pipeline = [
                {
                    "$bucket": {
                        "groupBy": "$Rate",
                        "boundaries": [0, 5, 6, 7, 8, 9, 10],
                        "default": "unknown",
                        "output": {
                            "count": {"$sum": 1},
                            "movies": {"$push": "$Title"}
                        }
                    }
                }
            ]
            results = list(self.collection.aggregate(pipeline))
            self.log(f"✓ Agregação: Distribuição de {len(results)} faixas de nota")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    def aggregation_cast_analysis(self):
        """Agregação: Análise de atores mais frequentes"""
        try:
            pipeline = [
                {"$limit": 100},  # Limita para performance
                {
                    "$project": {
                        "actors": {"$split": ["$Cast", "|"]},
                        "Rate": 1
                    }
                },
                {"$unwind": "$actors"},
                {
                    "$group": {
                        "_id": {"$trim": {"input": "$actors"}},
                        "count": {"$sum": 1},
                        "avg_rate": {"$avg": "$Rate"}
                    }
                },
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]
            results = list(self.collection.aggregate(pipeline))
            self.log(f"✓ Agregação: Top {len(results)} atores/atrizes")
            return results
        except Exception as e:
            self.log(f"✗ Erro na análise de cast: {str(e)}")
            return []
    
    def aggregation_metascore_correlation(self):
        """Agregação: Correlação Metascore vs Rate"""
        try:
            pipeline = [
                {"$match": {"Metascore": {"$exists": True, "$ne": None}}},
                {
                    "$bucket": {
                        "groupBy": "$Metascore",
                        "boundaries": [0, 50, 60, 70, 80, 90, 100],
                        "default": "unknown",
                        "output": {
                            "count": {"$sum": 1},
                            "avg_imdb_rate": {"$avg": "$Rate"}
                        }
                    }
                }
            ]
            results = list(self.collection.aggregate(pipeline))
            self.log(f"✓ Agregação: Correlação Metascore-Rate em {len(results)} faixas")
            return results
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return []
    
    # ===== ÍNDICES =====
    
    def create_text_index(self):
        """Cria índice de texto no título"""
        try:
            self.collection.create_index([("Title", "text")])
            self.log("✓ Índice de texto criado: Title")
            return True
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return False
    
    def create_sparse_index(self):
        """Cria índice sparse no Metascore"""
        try:
            self.collection.create_index("Metascore", sparse=True)
            self.log("✓ Índice sparse criado: Metascore")
            return True
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return False
    
    def get_index_statistics(self):
        """Obtém estatísticas dos índices"""
        try:
            stats = self.collection.index_information()
            self.log(f"✓ {len(stats)} índices encontrados")
            return stats
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return {}
    
    def get_collection_stats(self):
        """Obtém estatísticas da coleção"""
        try:
            stats = self.db.command("collStats", self.collection.name)
            self.log(f"✓ Estatísticas da coleção obtidas")
            return stats
        except Exception as e:
            self.log(f"✗ Erro: {str(e)}")
            return {}
    
    def save_results(self, filename="advanced_queries_results.txt"):
        """Salva resultados em arquivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.results_log))
            self.log(f"✓ Resultados salvos em: {filename}")
        except Exception as e:
            self.log(f"✗ Erro ao salvar: {str(e)}")
    
    def disconnect(self):
        """Desconecta do MongoDB"""
        if self.client:
            self.client.close()
            self.log("✓ Desconectado")


def main():
    """Executa operações avançadas"""
    USERNAME = "admin"
    PASSWORD = "admin"
    CLUSTER_URI = "cluster0.5kdvicj.mongodb.net"
    
    ops = AdvancedMongoDBOperations(USERNAME, PASSWORD, CLUSTER_URI)
    
    if not ops.connect("imdb", "movies"):
        return
    
    print("\n" + "="*60)
    print("CONSULTAS AVANÇADAS")
    print("="*60)
    
    print("\n--- Top 10 Filmes ---")
    top_10 = ops.query_top_10_movies()
    for i, movie in enumerate(top_10, 1):
        print(f"{i}. {movie['Title']} ({movie['Year']}) - {movie['Rate']}")
    
    print("\n--- Filmes com Metascore >= 90 ---")
    metascore = ops.query_movies_with_metascore(90)
    for movie in metascore[:5]:
        print(f"   {movie['Title']} - IMDb: {movie['Rate']}, Metascore: {movie['Metascore']}")
    
    print("\n--- Busca de Texto: 'War' ---")
    search = ops.query_text_search("War")
    for movie in search:
        print(f"   {movie['Title']} - {movie['Rate']}")
    
    print("\n" + "="*60)
    print("AGREGAÇÕES AVANÇADAS")
    print("="*60)
    
    print("\n--- Distribuição de Notas ---")
    dist = ops.aggregation_rating_distribution()
    for bucket in dist:
        if bucket['_id'] != 'unknown':
            print(f"   {bucket['_id']}: {bucket['count']} filmes")
    
    print("\n--- Top Atores/Atrizes ---")
    cast = ops.aggregation_cast_analysis()
    for i, actor in enumerate(cast, 1):
        print(f"{i}. {actor['_id']} - {actor['count']} filmes, média {actor['avg_rate']:.2f}")
    
    print("\n--- Combinações Certificado/Gênero ---")
    combos = ops.aggregation_movies_by_certificate_and_genre()
    for combo in combos[:5]:
        cert = combo['_id']['certificate']
        genre = combo['_id']['genre']
        print(f"   {cert} | {genre}: {combo['count']} filmes, média {combo['avg_rate']:.2f}")
    
    print("\n" + "="*60)
    print("ÍNDICES E ESTATÍSTICAS")
    print("="*60)
    
    ops.create_text_index()
    ops.create_sparse_index()
    
    print("\n--- Índices ---")
    indexes = ops.get_index_statistics()
    for index_name, index_info in indexes.items():
        print(f"   {index_name}: {index_info['key']}")
    
    print("\n--- Estatísticas da Coleção ---")
    stats = ops.get_collection_stats()
    if stats:
        print(f"   Documentos: {stats.get('count', 'N/A')}")
        print(f"   Tamanho: {stats.get('size', 'N/A')} bytes")
        print(f"   Índices: {stats.get('nindexes', 'N/A')}")
    
    ops.save_results()
    ops.disconnect()
    
    print("\n" + "="*60)
    print("Consultas avançadas concluídas!")
    print("="*60)


if __name__ == "__main__":
    main()
