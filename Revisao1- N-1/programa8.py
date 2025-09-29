valor = int(input("Digite um valor: "))

notas = [100, 50, 20, 10, 5, 2]

for nota in notas:
    qnt_notas = (valor // nota)
    valor = (valor % nota)
    if qnt_notas > 0:
        print(f"{qnt_notas} notas(a) de R$ {nota}")

if valor !=0:
    print(f"Não é possivel realizar o saque neste R$ {valor}!")