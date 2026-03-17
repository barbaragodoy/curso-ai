"""Exercício 5 – EMPTY
Um sistema técnico lida com uma pilha de chamados urgentes. Se a pilha estiver vazia,
ninguém precisa de atendimento agora.
Tarefa: Verifique se há chamados pendentes ou se está vazio.
Código funcional usando EMPTY:"""

def empty(pilha):
    return len(pilha) == 0

chamados = []
if empty(chamados):
    print("Nenhum chamado urgente no momento. (EMPTY)")
else:
    print("Chamados aguardando resolução!")