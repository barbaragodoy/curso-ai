"""Exercício 2 – SIZE
Uma impressora trabalha com uma pilha de documentos de emergência. Cada novo
documento é empilhado. Antes de iniciar, o sistema precisa saber quantos documentos tem
na pilha.
Tarefa: Mostre o número de documentos aguardando impressão.
Código funcional usando SIZE:"""

def size(pilha):
    return len(pilha)

documentos = ["Contrato.pdf", "Relatório.docx", "Proposta.xlsx"]
print("Número de documentos na fila (SIZE):", size(documentos))