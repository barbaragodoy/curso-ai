# Programa 24: Simulação de votação entre 20 eleitores
print("=== ELEIÇÃO ===")
print("Candidatos:")
print("1: Candidato A")
print("2: Candidato B") 
print("3: Candidato C")
print("4: Voto em Branco")
print("5: Voto Nulo")
print()

# Inicializar contadores
votos_a = 0
votos_b = 0
votos_c = 0
votos_branco = 0
votos_nulo = 0

# Coletar 20 votos
for eleitor in range(1, 21):
    while True:
        try:
            voto = int(input(f"Eleitor {eleitor}: Digite seu voto (1-5): "))
            if 1 <= voto <= 5:
                break
            else:
                print("Voto inválido! Digite um número entre 1 e 5.")
        except ValueError:
            print("Entrada inválida! Digite um número inteiro.")
    
    # Contar votos
    if voto == 1:
        votos_a += 1
    elif voto == 2:
        votos_b += 1
    elif voto == 3:
        votos_c += 1
    elif voto == 4:
        votos_branco += 1
    elif voto == 5:
        votos_nulo += 1

# Relatório final
print("\n=== RELATÓRIO DA ELEIÇÃO ===")
print(f"Votos para Candidato A: {votos_a}")
print(f"Votos para Candidato B: {votos_b}")
print(f"Votos para Candidato C: {votos_c}")
print(f"Votos em Branco: {votos_branco}")
print(f"Votos Nulos: {votos_nulo}")

# Determinar vencedor
votos_candidatos = [votos_a, votos_b, votos_c]
nomes_candidatos = ["Candidato A", "Candidato B", "Candidato C"]
max_votos = max(votos_candidatos)
vencedores = [i for i, votos in enumerate(votos_candidatos) if votos == max_votos]

if len(vencedores) == 1:
    print(f"\nVencedor: {nomes_candidatos[vencedores[0]]} com {max_votos} votos!")
else:
    print(f"\nEMPATE! Os seguintes candidatos obtiveram {max_votos} votos:")
    for i in vencedores:
        print(f"- {nomes_candidatos[i]}")

