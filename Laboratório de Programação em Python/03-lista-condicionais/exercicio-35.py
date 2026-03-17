# Exercício 35: Algoritmo que determina situação do aluno por frequência e nota

# Lê frequência e nota do aluno
frequencia = float(input("Digite a frequência (0-100%): "))
nota = float(input("Digite a nota (0.0-10.0): "))

# Determina a situação do aluno
if frequencia <= 75:
    situacao = "Reprovado"
elif frequencia < 100:
    if nota <= 3.0:
        situacao = "Reprovado"
    elif nota < 7.0:
        situacao = "Recuperação"
    else:  # nota >= 7.0
        situacao = "Aprovado"
else:  # frequencia == 100
    if nota <= 3.0:
        situacao = "Reprovado"
    elif nota < 7.0:
        situacao = "Recuperação"
    else:  # nota >= 7.0
        situacao = "Aprovado"

print(f"Frequência: {frequencia}%")
print(f"Nota: {nota}")
print(f"Situação: {situacao}")
