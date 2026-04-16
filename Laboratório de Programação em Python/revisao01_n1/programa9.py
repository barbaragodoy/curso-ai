
preco_gasolina = 6.19
preco_alcool = 3.99

tipo = input("Digite o tipo de combustível (G - Gasolina / A - Álcool): ")
litros = float(input("Digite a quantidade de litros: "))


if tipo == 'A':
    preco = preco_alcool
    if litros <= 20:
        desconto = 0.03
    else:
        desconto = 0.05

elif tipo == "G":
    preco = preco_gasolina
    if litros <= 20:
        desconto = 0.04
    else:
        desconto = 0.06
else:
    print("Tipo inválido!")
    preco = 0
    desconto = 0


total_bruto = preco * litros
total_com_desconto = total_bruto * (1 - desconto)

print(f"Valor a pagar: R${total_com_desconto:.2f}")