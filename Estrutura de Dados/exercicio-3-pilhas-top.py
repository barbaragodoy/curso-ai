"""Exercício 3 – TOP
Um editor de texto permite desfazer ações. Cada ação feita é empilhada. Quando o usuário
clica em 'Desfazer', ele visualiza a última ação.
Tarefa: Mostre qual foi a última ação feita (sem remover ainda).
Código funcional de exemplo usando TOP:"""

def top(pilha):
    return pilha[-1]

acoes = ["digitar 'Olá'", "negrito", "inserir imagem", "centralizar texto"]
print("Última ação feita (TOP):", top(acoes))