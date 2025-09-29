import math

x = float(input('Digite um número para o x: '))
y = float(input('Digite um número para o y: '))
z = float(input('Digite um número para o z: '))
w = float(input('Digite um número para o w: '))

#numerador
quadrado_x = (x*x)
cubo_y = (y*y*y)
somar_x_y = (quadrado_x + cubo_y)
raiz = math.sqrt(somar_x_y)
potencia = (2**z)
numerador = raiz + potencia

#denominador

somar_w = (w + 5)

if somar_w == 0:
    print("Erro: divisão por zero. O denominador não pode ser zero.")
else:
    denominador = somar_w ** (1/3)

    # 5. Dividir numerador pelo denominador
    E = numerador / denominador

    # 6. Exibir resultado com 4 casas decimais
    print(f"E: {E:.4f}")