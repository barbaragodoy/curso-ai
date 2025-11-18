# =========================================================
# Sistema de Análise de Temperaturas da Empresa Climática TempTrack
# Implementação em Python baseada no documento "Revisao N2.pdf"
# =========================================================

# 1. Estrutura em Matriz

dados_temp = [
    ["Recife", 33, 35, 36, 34, 37],
    ["Salvador", 31, 32, 33, 32, 34],
    ["Rio de Janeiro", 36, 38, 37, 39, 40],
    ["São Paulo", 28, 29, 30, 31, 29],
    ["Manaus", 34, 36, 37, 38, 36]
]

# Variáveis globais para armazenar os resultados absolutos e totais
maior_temp_absoluta = -1
cidade_mais_quente_absoluta = ""
total_todas_temperaturas = 0  # Usado para a Média Geral
total_medicoes = 0           # Total de temperaturas na matriz (5 dias * 5 cidades = 25)

# 2. Função de Processamento
def processar(dados):
    global maior_temp_absoluta
    global cidade_mais_quente_absoluta
    global total_todas_temperaturas
    global total_medicoes
    
    # Reinicializa os contadores gerais no início da função para evitar erros
    total_todas_temperaturas = 0
    total_medicoes = 0
    
    resultados_cidades = []
    cidades_onda_calor = []
    
    for linha in dados:
        cidade = linha[0]
        # As temperaturas estão do índice 1 em diante (t1 até t5)
        temperaturas = linha[1:]
        
        # 2a) Calcular a média de temperatura de cada cidade
        soma_temperaturas = sum(temperaturas)
        num_dias = len(temperaturas)
        
        media = soma_temperaturas / num_dias
        
        # Atualiza os contadores globais para Média Geral (4. Cálculos Gerais)
        total_todas_temperaturas += soma_temperaturas
        total_medicoes += num_dias
        
        # 2b) Determinar a maior temperatura registrada na cidade
        maior_temp_local = max(temperaturas)

        # 3. Condicionais - Classificação Climática
        if media > 35:
            situacao = "Onda de Calor"
            # 2d) Montar e retornar lista de cidades em onda de calor
            cidades_onda_calor.append(cidade)
            # 2e) Exibir alerta durante o processamento
            print(f"ALERTA: Onda de calor em {cidade}")
        else:
            situacao = "Normal"
        
        # 2b) e 2c) Determinar a maior temperatura absoluta e a cidade mais quente
        if maior_temp_local > maior_temp_absoluta:
            maior_temp_absoluta = maior_temp_local
            cidade_mais_quente_absoluta = cidade
            
        # Adicionar resultados para serem retornados ao programa principal
        # Os dados retornados permitirão gerar o Relatório Completo (5. Saída Final)
        resultados_cidades.append([
            cidade, 
            round(media, 2),  # Arredonda a média para duas casas decimais
            maior_temp_local, 
            situacao
        ])
        
    return resultados_cidades, cidades_onda_calor

# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

print("--- INICIANDO ANÁLISE DE TEMPERATURAS (TempTrack) ---\n")

# Executa a função de processamento
relatorio_cidades, cidades_calor = processar(dados_temp)

print("\n--- PROCESSAMENTO DE DADOS CONCLUÍDO ---\n")

# 4. Cálculos Gerais Após a Função
print("=========================================")
print("         DADOS ESTATÍSTICOS GERAIS       ")
print("=========================================")

# A cidade mais quente da semana (retornada indiretamente via global)
print(f"Cidade mais quente da semana: {cidade_mais_quente_absoluta}")
# A maior temperatura absoluta registrada (retornada indiretamente via global)
print(f"Maior temperatura absoluta registrada: {maior_temp_absoluta} °C")

# Média geral das temperaturas máximas
if total_medicoes > 0:
    # Fórmula: Soma de todas as temperaturas / Total de medições
    media_geral = total_todas_temperaturas / total_medicoes
    print(f"Média geral das temperaturas máximas: {round(media_geral, 2)} °C")
else:
    print("Média geral: Não foi possível calcular (nenhuma medição encontrada).")

# O total de medições analisadas
print(f"Total de medições analisadas: {total_medicoes}")

# 5. Saída Final - Relatório Completo
print("\n=========================================")
print("           RELATÓRIO COMPLETO            ")
print("=========================================")
# Formatação da tabela: Alinhamento e espaçamento
print(f"{'Cidade':<18} | {'Média (°C)':<10} | {'Temp. Máx':<10} | Situação Climática")
print("-" * 55)

# Exibe o relatório cidade por cidade
for cidade, media, max_temp, situacao in relatorio_cidades:
    # 5. Saída Final (Nome, Média, Maior Temp, Situação Climática)
    print(f"{cidade:<18} | {media:<10} | {max_temp:<10} | {situacao}")

print("-" * 55)

# Exibe o resumo das cidades em onda de calor
if cidades_calor:
    print("\nResumo das Cidades em Onda de Calor:")
    print(", ".join(cidades_calor))
else:
    print("\nNenhuma cidade classificada em Onda de Calor.")

# FIM DO PROGRAMA
