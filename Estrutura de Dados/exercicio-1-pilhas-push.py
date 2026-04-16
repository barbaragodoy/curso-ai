"""Exercício 1 – PUSH
Um navegador salva o histórico das páginas visitadas usando uma pilha. Sempre que você
acessa uma nova página, ela é empilhada.
Tarefa: Simule o acesso a 3 páginas diferentes e mostre a pilha de histórico.
Código funcional de exemplo usando PUSH (append em Python):"""

def push(pilha, pagina):
    pilha.append(pagina)

historico = []
push(historico, "google.com")
push(historico, "youtube.com")
push(historico, "github.com")
print("Histórico de navegação (PUSH):", historico)