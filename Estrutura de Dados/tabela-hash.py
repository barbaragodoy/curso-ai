
"""Objetivo da atividade:

 ->Utilizando as funções já implementadas, os alunos devem:
 ->Buscar e imprimir os dados completos de um CPF específico presente na tabela hash.
 ->Remover um CPF da tabela hash.
 ->Verificar se a remoção foi realizada corretamente, tentando buscar novamente o CPF removido (o resultado esperado deve indicar que o CPF não está mais na tabela)."""


# Função que calcula o índice da tabela hash com base no CPF
def hash_function(cpf, table_size):  # Recebe um CPF e o tamanho da tabela
    return cpf % table_size  # Retorna o resto da divisão do CPF pelo tamanho da tabela (índice)

# Criando a tabela hash como uma lista de listas (estrutura com encadeamento separado)
table_size = 10  # Definimos o tamanho da tabela como 10 posições (buckets)
tabela_hash = [[] for _ in range(table_size)]  # Criamos a tabela: uma lista de 10 listas vazias (cada bucket é uma lista)

# Função para inserir um paciente na tabela hash
def inserir_paciente(cpf, dados):  # Recebe o CPF (chave) e os dados do paciente (valor)
    indice = hash_function(cpf, table_size)  # Calcula o índice onde o par será armazenado usando a função hash
    tabela_hash[indice].append((cpf, dados))  # Adiciona o par (cpf, dados) na lista correspondente ao índice

# Função para buscar um paciente na tabela hash usando o CPF
def buscar_paciente(cpf):  # Recebe o CPF que será buscado
    indice = hash_function(cpf, table_size)  # Calcula o índice correspondente usando a função hash
    for chave, valor in tabela_hash[indice]:  # Percorre a lista de pares armazenada no índice
        if chave == cpf:  # Se encontrar um par onde a chave (CPF) é igual ao CPF buscado
            return valor  # Retorna os dados do paciente encontrados
    return None  # Se não encontrar, retorna None (não encontrado)

# Função para remover um paciente da tabela hash usando o CPF
def remover_paciente(cpf):  # Recebe o CPF que será removido
    indice = hash_function(cpf, table_size)  # Calcula o índice correspondente usando a função hash
    for i, (chave, _) in enumerate(tabela_hash[indice]):  # Percorre a lista de pares no índice, com índice de posição
        if chave == cpf:  # Se encontrar o par com o CPF desejado
            del tabela_hash[indice][i]  # Remove o par da lista
            return True  # Retorna True indicando que a remoção foi bem-sucedida
    return False  # Se não encontrar, retorna False (nada foi removido)

# Inserindo alguns CPFs na tabela hash
inserir_paciente(12345678901, {"nome": "Ana", "idade": 30, "condicao": "Estável"})  # Insere o CPF 12345678901 com dados da Ana
inserir_paciente(98765432100, {"nome": "Bruno", "idade": 45, "condicao": "Emergência"})  # Insere o CPF 98765432100 com dados do Bruno
inserir_paciente(11122233344, {"nome": "Carlos", "idade": 50, "condicao": "Observação"})  # Insere o CPF 11122233344 com dados do Carlos

# ===== PROGRAMA PRINCIPAL =====
# Demonstrando as operações solicitadas na atividade

print("=" * 50)
print("DEMONSTRAÇÃO DAS OPERAÇÕES DA TABELA HASH")
print("=" * 50)

# 1. Buscar e imprimir os dados completos de um CPF específico
print("\n1. BUSCAR E IMPRIMIR DADOS DE UM CPF")
print("-" * 50)
cpf_busca = 98765432100  # CPF do Bruno
dados_encontrados = buscar_paciente(cpf_busca)

if dados_encontrados:
    print(f"CPF {cpf_busca} encontrado!")
    print("Dados completos do paciente:")
    for chave, valor in dados_encontrados.items():
        print(f"  {chave.capitalize()}: {valor}")
else:
    print(f"CPF {cpf_busca} não encontrado na tabela.")

# 2. Remover um CPF da tabela hash
print("\n2. REMOVER UM CPF DA TABELA HASH")
print("-" * 50)
cpf_remover = 98765432100  # Vamos remover o CPF do Bruno
resultado_remocao = remover_paciente(cpf_remover)

if resultado_remocao:
    print(f"CPF {cpf_remover} removido com sucesso!")
else:
    print(f"CPF {cpf_remover} não encontrado para remoção.")

# 3. Verificar se a remoção foi realizada corretamente
print("\n3. VERIFICAR SE A REMOÇÃO FOI REALIZADA CORRETAMENTE")
print("-" * 50)
print(f"Tentando buscar novamente o CPF {cpf_remover} removido...")
dados_apos_remocao = buscar_paciente(cpf_remover)

if dados_apos_remocao:
    print(f"ERRO: CPF {cpf_remover} ainda está na tabela!")
else:
    print(f"✓ SUCESSO: CPF {cpf_remover} não está mais na tabela.")
    print("A remoção foi realizada corretamente!")

print("\n" + "=" * 50)