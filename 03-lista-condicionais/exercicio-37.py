# Exercício 37: Algoritmo que converte número em dia da semana

# Lê um número entre 1 e 7
numero = int(input("Digite um número entre 1 e 7: "))

# Converte o número em dia da semana
if numero == 1:
    dia = "Domingo"
elif numero == 2:
    dia = "Segunda-feira"
elif numero == 3:
    dia = "Terça-feira"
elif numero == 4:
    dia = "Quarta-feira"
elif numero == 5:
    dia = "Quinta-feira"
elif numero == 6:
    dia = "Sexta-feira"
elif numero == 7:
    dia = "Sábado"
else:
    dia = "Não existe dia da semana com esse número"

print(f"Dia da semana: {dia}")
