"""
Aprendizagem de Máquina – Supervisionada - Exercício: Classificação e Regressão

Objetivo: Usar scikit-learn para treinar um modelo simples de classificação
e um de regressão (exemplo com dados sintéticos).
"""

# Descomente e instale se necessário: pip install scikit-learn
# from sklearn.datasets import make_classification, make_regression
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression, LinearRegression
# from sklearn.metrics import accuracy_score, mean_squared_error


def exercicio_classificacao():
    """Exemplo de pipeline de classificação supervisionada."""
    # X, y = make_classification(n_samples=100, n_features=4, random_state=42)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # model = LogisticRegression().fit(X_train, y_train)
    # pred = model.predict(X_test)
    # print("Acurácia:", accuracy_score(y_test, pred))
    print("Pipeline: dados -> treino -> predição -> métrica (acurácia).")
    print("Substitua por código real usando sklearn quando o ambiente estiver pronto.")


def exercicio_regressao():
    """Exemplo de pipeline de regressão supervisionada."""
    # X, y = make_regression(n_samples=100, n_features=2, noise=10, random_state=42)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    # model = LinearRegression().fit(X_train, y_train)
    # pred = model.predict(X_test)
    # print("MSE:", mean_squared_error(y_test, pred))
    print("Pipeline: dados -> treino -> predição -> métrica (MSE).")
    print("Substitua por código real usando sklearn quando o ambiente estiver pronto.")


if __name__ == "__main__":
    print("=== Classificação (ex.: LogisticRegression) ===")
    exercicio_classificacao()
    print("\n=== Regressão (ex.: LinearRegression) ===")
    exercicio_regressao()
