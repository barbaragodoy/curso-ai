# ========================================
# ATIVIDADE 5 - Quinta Atividade do Curso
# Objetivo: Cálculo de divisão com quociente e resto
# ========================================

# Recebe dois números inteiros do usuário
numero1 = int(input("Insira um número"))
numero2 = int(input("Insira um número"))

# Define as variáveis para melhor compreensão
dividendo = (numero1)  # Número que será dividido
divisor = (numero2)    # Número pelo qual será dividido

# Calcula o quociente (resultado da divisão)
quociente = (numero1 / numero2)
# Calcula o resto da divisão
resto = (numero1 % numero2)

# Exibe todos os valores da operação de divisão
print ("O dividendo é " , dividendo, "o divisor é" , divisor, "o quociente é" , quociente, "e o resto é" , resto )