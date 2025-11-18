# Exercício 26: Algoritmo que calcula média semestral e determina situação

# Lê as duas notas bimestrais
nota1 = float(input("Digite a primeira nota bimestral: "))
nota2 = float(input("Digite a segunda nota bimestral: "))

# Calcula a média semestral
media = (nota1 + nota2) / 2

# Determina a situação
if media >= 7:
    situacao = "Aprovado"
elif media < 3:
    situacao = "Reprovado"
else:
    situacao = "Recuperação"

print(f"Média semestral: {media:.2f}")
print(f"Situação: {situacao}")
