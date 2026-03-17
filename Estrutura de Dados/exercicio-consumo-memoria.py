import sys  # Importamos o módulo sys

# Criamos uma lista simples
minha_lista = [0, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80]

# Verificamos o tamanho da lista em bytes
tamanho = sys.getsizeof(minha_lista)

# Exibimos o tamanho
print("O tamanho da lista em memória é:", tamanho, "bytes")