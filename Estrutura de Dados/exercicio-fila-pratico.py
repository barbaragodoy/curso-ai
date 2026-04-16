# Exercício 1 - ENQUEUE (Enfileirar)
# Situação real: Uma fila para comprar ingresso no cinema. Uma nova pessoa chega e entra no final da fila.
# O comando 'append' serve para adicionar um elemento no final de uma lista (fila).

fila = ["João", "Maria", "José"]  # Cria a fila inicial
print("Fila inicial:", fila)  # Mostra a fila inicial

novo_cliente = "Ana"  # Define um novo cliente que chegou
fila.append(novo_cliente)  # Adiciona Ana ao final da fila

print("Fila após chegada de Ana:", fila)  # Mostra a fila atualizada

#---------------------------
# Exercício 2 - SIZE (Tamanho)
# Situação real: Um atendente quer saber quantas pessoas ainda estão aguardando atendimento na fila do banco.
# O comando 'len' serve para contar o número de elementos de uma lista (fila).

fila_banco = ["Cliente1", "Cliente2", "Cliente3", "Cliente4"]  # Clientes que aguardam

tamanho_fila = len(fila_banco)  # Conta quantos clientes estão aguardando

print("Quantidade de clientes aguardando:", tamanho_fila)  # Mostra o tamanho da fila
#---------------------------
# Exercício 3 - HEAD (Cabeça da fila)
# Situação real: Saber quem será a próxima pessoa a ser atendida no caixa do supermercado.
# O comando '[0]' acessa o primeiro elemento da lista (o início da fila).

fila_mercado = ["Pedro", "Lucas", "Mariana"]  # Clientes esperando

proximo_cliente = fila_mercado[0]  # Acessa o primeiro da fila

print("Próximo cliente a ser atendido:", proximo_cliente)  # Mostra quem está no início
#---------------------------
# Exercício 4 - DEQUEUE (Desenfileirar)
# Situação real: A primeira pessoa da fila entra no consultório médico e sai da fila.
# O comando 'pop(0)' remove o primeiro elemento da lista (inicio da fila).

fila_consultorio = ["Paciente1", "Paciente2", "Paciente3"]  # Pacientes esperando
print("Fila antes do atendimento:", fila_consultorio)  # Mostra a fila antes do atendimento

paciente_atendido = fila_consultorio.pop(0)  # Remove o primeiro paciente da fila

print("Paciente atendido:", paciente_atendido)  # Exibe o paciente que saiu
print("Fila após atendimento:", fila_consultorio)  # Mostra a fila atualizada
#---------------------------
# Exercício 5 - EMPTY (Verificar se está vazia)
# Situação real: Uma secretária verifica se ainda há pacientes na sala de espera do consultório.
# O comando 'len' verifica se o número de elementos é zero (fila vazia).

fila_sala_espera = []  # Fila vazia

# O operador == serve para comparar dois valores e verificar se eles são iguais.
# Por exemplo, a expressão len(fila_sala_espera) == 0 verifica se o tamanho da fila é igual a zero.

# Já o operador = é usado para atribuir um valor a uma variável.
# Por exemplo, fila = [] significa que você está atribuindo uma lista vazia à variável fila.

if len(fila_sala_espera) == 0:  # Verifica se a fila está vazia
    print("A sala de espera está vazia.")  # Exibe mensagem de fila vazia
else:
    print("Ainda há pacientes aguardando.")  # Exibe mensagem caso ainda tenha alguém