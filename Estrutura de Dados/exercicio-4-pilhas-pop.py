"""Exercício 4 – POP
Durante o desenvolvimento, um programador quer desfazer as 3 últimas alterações que ele
empilhou como ações. Para isso, ele vai usando POP para desfazer.
Tarefa: Remova as últimas 3 ações usando POP.
Código de exemplo funcional:"""

alteracoes = ["adicionar função", "renomear variável", "ajustar identação", "remover comentário"]
print("Desfazendo:", alteracoes.pop())
print("Desfazendo:", alteracoes.pop())
print("Desfazendo:", alteracoes.pop())
print("Alterações restantes:", alteracoes)