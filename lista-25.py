
numero = int(input("Digite um número de 3 dígitos: "))


centena = numero // 100
dezena  = (numero // 10) % 10
unidade = numero % 10


invertido = unidade * 100 + dezena * 10 + centena


print("Número invertido:", invertido)