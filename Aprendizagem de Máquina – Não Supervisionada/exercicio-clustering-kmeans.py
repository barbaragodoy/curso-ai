"""
Aprendizagem de Máquina – Não Supervisionada - Exercício: Clustering (K-Means)

Objetivo: Agrupar dados sem rótulos usando K-Means.
Clustering é não supervisionado: não usamos respostas conhecidas, apenas a estrutura dos dados.
"""

# Descomente e instale se necessário: pip install scikit-learn
# from sklearn.datasets import make_blobs
# from sklearn.cluster import KMeans
# import matplotlib.pyplot as plt


def exercicio_kmeans():
    """
    Exemplo: gerar blobs, aplicar K-Means e (opcional) visualizar clusters.
    """
    # X, _ = make_blobs(n_samples=300, centers=4, random_state=42)
    # kmeans = KMeans(n_clusters=4, random_state=42).fit(X)
    # labels = kmeans.labels_
    # centros = kmeans.cluster_centers_
    # print("Centros dos clusters:\n", centros)
    # print("Rótulos (primeiros 10):", labels[:10])
    print("K-Means: agrupa pontos em K clusters sem usar rótulos.")
    print("Métricas comuns: inércia, silhueta. Substitua por código sklearn quando possível.")


if __name__ == "__main__":
    print("=== Clustering não supervisionado (K-Means) ===")
    exercicio_kmeans()
