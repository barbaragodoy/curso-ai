# Sistema de Análise Semanal de Treinos da Academia Senai Fitness

# -----------------------------
# 1) Leitura / armazenamento dos dados (lista de listas)
# -----------------------------
dados_semana = [
    ["João",   "Agachamento", 120, 350],
    ["João",   "Flexão",       80, 200],
    ["João",   "Corrida",      30, 450],
    ["Maria",  "Corrida",      45, 600],
    ["Maria",  "Abdominal",   200, 300],
    ["Carlos", "Flexão",      150, 380],
    ["Carlos", "Corrida",      60, 850],
    ["Carlos", "Agachamento",  90, 270],
    ["Ana",    "Abdominal",   250, 380],
    ["Ana",    "Corrida",      20, 300],
    ["Ana",    "Burpee",       40, 420],
    ["Pedro",  "Corrida",      80, 900],
    ["Pedro",  "Agachamento", 100, 320],
    ["Pedro",  "Flexão",       50, 150],
]

# -----------------------------
# 2) Funções de processamento
# -----------------------------

def calcular_totais_por_aluno(dados):
    """
    Retorna um dicionário no formato:
    {
        "João": {"repeticoes": total_reps, "calorias": total_cal},
        ...
    }
    """
    totais = {}

    for aluno, exercicio, repeticoes, calorias in dados:
        if aluno not in totais:
            totais[aluno] = {"repeticoes": 0, "calorias": 0}

        totais[aluno]["repeticoes"] += repeticoes
        totais[aluno]["calorias"] += calorias

    return totais


def total_calorias_por_aluno(dados):
    totais = calcular_totais_por_aluno(dados)
    resultado = {}
    for aluno, info in totais.items():
        resultado[aluno] = info["calorias"]
    return resultado


def total_repeticoes_por_aluno(dados):
    totais = calcular_totais_por_aluno(dados)
    resultado = {}
    for aluno, info in totais.items():
        resultado[aluno] = info["repeticoes"]
    return resultado


def classificar_aluno(total_calorias):
    """
    Classificação conforme o enunciado:
    >= 2000      -> Desempenho Excelente
    1200–1999    -> Bom Desempenho
    < 1200       -> Desempenho Baixo
    """
    if total_calorias >= 2000:
        return "Desempenho Excelente"
    elif 1200 <= total_calorias <= 1999:
        return "Bom Desempenho"
    else:
        return "Desempenho Baixo"


def aluno_que_mais_gastou_calorias(totais):
    """
    Recebe o dicionário de totais_por_aluno e
    devolve (nome_do_aluno, calorias).
    """
    maior_aluno = None
    maior_calorias = -1

    for aluno, info in totais.items():
        if info["calorias"] > maior_calorias:
            maior_calorias = info["calorias"]
            maior_aluno = aluno

    return maior_aluno, maior_calorias


# -----------------------------
# 3) Saída final (relatório)
# -----------------------------
def main():
    # Calcula totais
    totais_por_aluno = calcular_totais_por_aluno(dados_semana)

    print("=== Relatório Semanal de Treinos ===\n")

    for aluno, info in totais_por_aluno.items():
        total_reps = info["repeticoes"]
        total_cal = info["calorias"]
        classificacao = classificar_aluno(total_cal)

        print(f"Aluno: {aluno}")
        print(f"  Total de repetições: {total_reps}")
        print(f"  Total de calorias:   {total_cal}")
        print(f"  Classificação final: {classificacao}")
        print("-" * 40)

    # Aluno que mais gastou calorias
    melhor_aluno, maior_calorias = aluno_que_mais_gastou_calorias(totais_por_aluno)
    print(f"\nAluno que mais gastou calorias na semana: {melhor_aluno} ({maior_calorias} calorias)")


if __name__ == "__main__":
    main()
