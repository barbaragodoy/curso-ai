
conta = 235

centena = conta // 100
dezena  = (conta // 10) % 10
unidade = conta % 10


inverso = unidade * 100 + dezena * 10 + centena


soma = conta + inverso   

d1 = soma // 100        
d2 = (soma // 10) % 10  
d3 = soma % 10         


total = d1*1 + d2*2 + d3*3


digito_verificador = total % 10

print("Conta:", conta)
print("Inverso:", inverso)
print("Soma:", soma)
print("Resultado ponderado:", total)
print("Dígito verificador:", digito_verificador)


