# -*- coding: utf-8 -*-
"""
ANALISE DE DADOS IDEB - GOIAS
Índice de Desenvolvimento da Educação Básica (2005-2023)

Script para:
1. Importar dados de consulta.csv
2. Processar e limpar dados
3. Calcular KPIs
4. Gerar gráficos
5. Exportar dados processados
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 6)
plt.rcParams['font.size'] = 10

print("=" * 80)
print("ANALISE DE DADOS IDEB - GOIAS (2005-2023)")
print("=" * 80)
print()


# PASSO 1: IMPORTACAO E LIMPEZA DE DADOS

print("PASSO 1: IMPORTACAO E LIMPEZA DE DADOS")
print("-" * 80)

# Ler arquivo CSV
try:
    df_raw = pd.read_csv('consulta.csv', sep=';', encoding='latin-1')
    print("[OK] Arquivo carregado: consulta.csv")
    print("Dimensoes: {} linhas x {} colunas".format(df_raw.shape[0], df_raw.shape[1]))
except FileNotFoundError:
    print("[ERRO] Arquivo consulta.csv nao encontrado!")
    exit(1)

print()


# PASSO 2: TRANSFORMACAO DE DADOS

print("PASSO 2: TRANSFORMACAO DE DADOS")
print("-" * 80)

# Corrigir nomes das colunas
df_raw.columns = ['Localidade', 'Variavel'] + list(df_raw.columns[2:])

# Processar dados
registros = []
anos_cols = ['2005', '2007', '2009', '2011', '2013', '2015', '2017', '2019', '2021', '2023']

for idx, row in df_raw.iterrows():
    localidade = row['Localidade'].strip()
    variavel = row['Variavel'].strip()
    
    # Extrair tipo (Municipal ou Estadual)
    tipo = 'Municipal' if 'Municipal' in variavel else 'Estadual'
    
    # Processar cada ano
    for ano in anos_cols:
        valor_str = str(row[ano]).strip()
        
        # Converter valor (tratar "-" como NaN)
        if valor_str == '-':
            valor = np.nan
        else:
            try:
                valor = float(valor_str.replace(',', '.'))
            except:
                valor = np.nan
        
        registros.append({
            'Ano': int(ano),
            'Localidade': localidade,
            'Tipo': tipo,
            'IDEB': valor
        })

# Criar dataframe processado
df = pd.DataFrame(registros)

print("[OK] Dados transformados")
print("Linhas: {}".format(len(df)))
print("Colunas: {}".format(len(df.columns)))
print()


# PASSO 3: ANALISE EXPLORATORIA

print("PASSO 3: ANALISE EXPLORATORIA")
print("-" * 80)

print("\nESTATISTICAS DESCRITIVAS:")
stats = df.describe().round(2)
print(stats)
print()

print("INFORMACOES POR LOCALIDADE E TIPO:")
for localidade in sorted(df['Localidade'].unique()):
    print("\n[LOCALIDADE] {}".format(localidade))
    for tipo in ['Municipal', 'Estadual']:
        df_filtro = df[(df['Localidade'] == localidade) & (df['Tipo'] == tipo)]
        if len(df_filtro) > 0:
            print("  [{}]".format(tipo))
            print("    Minimo IDEB: {:.1f}".format(df_filtro['IDEB'].min()))
            print("    Maximo IDEB: {:.1f}".format(df_filtro['IDEB'].max()))
            print("    Media IDEB: {:.2f}".format(df_filtro['IDEB'].mean()))
            
            # Calcular variação 2005-2023
            ideb_2005 = df_filtro[df_filtro['Ano'] == 2005]['IDEB'].values
            ideb_2023 = df_filtro[df_filtro['Ano'] == 2023]['IDEB'].values
            if len(ideb_2005) > 0 and len(ideb_2023) > 0 and not np.isnan(ideb_2023[0]):
                variacao = ideb_2023[0] - ideb_2005[0]
                pct = (variacao / ideb_2005[0]) * 100
                print("    Variacao (2005-2023): {:.2f} ({:.1f}%)".format(variacao, pct))

print()


# PASSO 4: CALCULAR KPIs

print("PASSO 4: CALCULO DE KPIs")
print("-" * 80)

print("\nKPI 1: EVOLUCAO DO IDEB (2005-2023)")
print()

for localidade in sorted(df['Localidade'].unique()):
    for tipo in ['Municipal', 'Estadual']:
        df_kpi = df[(df['Localidade'] == localidade) & (df['Tipo'] == tipo)]
        ideb_2005 = df_kpi[df_kpi['Ano'] == 2005]['IDEB'].values
        ideb_2023 = df_kpi[df_kpi['Ano'] == 2023]['IDEB'].values
        
        if len(ideb_2005) > 0 and len(ideb_2023) > 0 and not np.isnan(ideb_2023[0]):
            var = ideb_2023[0] - ideb_2005[0]
            pct = (var / ideb_2005[0]) * 100
            print("  {} ({}): {:.1f} -> {:.1f} | Variacao: {:.2f} ({:.1f}%)".format(
                localidade, tipo, ideb_2005[0], ideb_2023[0], var, pct))

print("\nKPI 2: DESEMPENHO 2023")
print()

df_2023 = df[df['Ano'] == 2023].dropna()
for idx, row in df_2023.iterrows():
    print("  {} ({}): {:.1f}".format(row['Localidade'], row['Tipo'], row['IDEB']))

print("\nKPI 3: CONSISTENCIA DO DESEMPENHO (Desvio Padrao)")
print()

for localidade in sorted(df['Localidade'].unique()):
    for tipo in ['Municipal', 'Estadual']:
        df_cons = df[(df['Localidade'] == localidade) & (df['Tipo'] == tipo)]
        std = df_cons['IDEB'].std()
        mean = df_cons['IDEB'].mean()
        cv = (std / mean) * 100
        
        print("  {} ({}): Desvio={:.2f} | CV={:.2f}%".format(
            localidade, tipo, std, cv))

print()


# PASSO 5: GERAR GRAFICOS

print("PASSO 5: GERANDO GRAFICOS")
print("-" * 80)

# Obter localidades unicas
locais_unique = sorted(df['Localidade'].unique())

# Grafico 1: Caldas Novas
fig, ax = plt.subplots(figsize=(14, 6))
df_caldas = df[df['Localidade'] == locais_unique[0]].sort_values('Ano')

for tipo in ['Municipal', 'Estadual']:
    df_tipo = df_caldas[df_caldas['Tipo'] == tipo]
    if len(df_tipo) > 0:
        ax.plot(df_tipo['Ano'], df_tipo['IDEB'], 
                marker='o', linewidth=2.5, label=tipo, markersize=8)

ax.set_title('Evolucao IDEB - {}\nEnsino Fundamental - Anos Iniciais (2005-2023)'.format(locais_unique[0]), 
             fontsize=13, fontweight='bold')
ax.set_xlabel('Ano', fontsize=11)
ax.set_ylabel('IDEB', fontsize=11)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(df['Ano'].unique()))
ax.set_ylim([3, 7.5])

plt.tight_layout()
plt.savefig('01_caldas_novas_ideb.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 01_caldas_novas_ideb.png")

# Grafico 2: Goiania
fig, ax = plt.subplots(figsize=(14, 6))
df_goiania = df[df['Localidade'] == locais_unique[1]].sort_values('Ano')

for tipo in ['Municipal', 'Estadual']:
    df_tipo = df_goiania[df_goiania['Tipo'] == tipo]
    if len(df_tipo) > 0:
        ax.plot(df_tipo['Ano'], df_tipo['IDEB'], 
                marker='s', linewidth=2.5, label=tipo, markersize=8)

ax.set_title('Evolucao IDEB - {}\nEnsino Fundamental - Anos Iniciais (2005-2023)'.format(locais_unique[1]), 
             fontsize=13, fontweight='bold')
ax.set_xlabel('Ano', fontsize=11)
ax.set_ylabel('IDEB', fontsize=11)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(df['Ano'].unique()))
ax.set_ylim([3, 7.5])

plt.tight_layout()
plt.savefig('02_goiania_ideb.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 02_goiania_ideb.png")

# Grafico 3: Comparativo 2023
fig, ax = plt.subplots(figsize=(12, 6))

df_2023_plot = df[df['Ano'] == 2023].dropna()

municipais = []
estaduais = []

for localidade in locais_unique:
    mun = df_2023_plot[(df_2023_plot['Localidade'] == localidade) & 
                       (df_2023_plot['Tipo'] == 'Municipal')]['IDEB'].values
    est = df_2023_plot[(df_2023_plot['Localidade'] == localidade) & 
                       (df_2023_plot['Tipo'] == 'Estadual')]['IDEB'].values
    
    if len(mun) > 0:
        municipais.append(mun[0])
    else:
        municipais.append(np.nan)
    
    if len(est) > 0:
        estaduais.append(est[0])
    else:
        estaduais.append(np.nan)

x = np.arange(len(locais_unique))
width = 0.35

bars1 = ax.bar(x - width/2, municipais, width, label='Municipal', color='#2E86AB')
bars2 = ax.bar(x + width/2, estaduais, width, label='Estadual', color='#A23B72')

ax.set_ylabel('IDEB', fontsize=11)
ax.set_title('Comparativo IDEB 2023 - Redes Municipal e Estadual', 
             fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(locais_unique)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
ax.set_ylim([0, 7.5])

for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        if not np.isnan(height):
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    '{:.1f}'.format(height), ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('03_comparativo_2023.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 03_comparativo_2023.png")

# Grafico 4: Todas as series
fig, ax = plt.subplots(figsize=(14, 6))

cores = {locais_unique[0]: '#1F77B4', locais_unique[1]: '#FF7F0E'}
marcadores = {'Municipal': 'o', 'Estadual': 's'}

for localidade in locais_unique:
    for tipo in ['Municipal', 'Estadual']:
        df_plot = df[(df['Localidade'] == localidade) & (df['Tipo'] == tipo)].sort_values('Ano')
        if len(df_plot) > 0:
            label = "{} - {}".format(localidade, tipo)
            ax.plot(df_plot['Ano'], df_plot['IDEB'], 
                    marker=marcadores[tipo], linewidth=2, label=label, 
                    color=cores[localidade], markersize=7)

ax.set_title('Evolucao IDEB (2005-2023) - Todas as Series', fontsize=13, fontweight='bold')
ax.set_xlabel('Ano', fontsize=11)
ax.set_ylabel('IDEB', fontsize=11)
ax.legend(fontsize=10, loc='best', ncol=2)
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(df['Ano'].unique()))

plt.tight_layout()
plt.savefig('04_todas_series.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 04_todas_series.png")

# Grafico 5: Box plot
fig, ax = plt.subplots(figsize=(12, 6))

dados_box = []
labels_box = []

for localidade in locais_unique:
    for tipo in ['Municipal', 'Estadual']:
        df_box = df[(df['Localidade'] == localidade) & (df['Tipo'] == tipo)]['IDEB'].dropna()
        if len(df_box) > 0:
            dados_box.append(df_box.values)
            labels_box.append("{}\n{}".format(localidade, tipo))

bp = ax.boxplot(dados_box, tick_labels=labels_box, patch_artist=True)

colors = ['#2E86AB', '#A23B72', '#2E86AB', '#A23B72']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_ylabel('IDEB', fontsize=11)
ax.set_title('Distribuicao IDEB por Localidade e Tipo (2005-2023)', 
             fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('05_distribuicao_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()
print("[OK] 05_distribuicao_boxplot.png")

print()


# PASSO 6: EXPORTAR DADOS

print("PASSO 6: EXPORTACAO DE DADOS")
print("-" * 80)

# Exportar em CSV
df.to_csv('01_dataset_ideb_processado.csv', sep=';', encoding='utf-8', index=False)
print("[OK] 01_dataset_ideb_processado.csv")

# Exportar em Excel
try:
    df.to_excel('01_dataset_ideb_processado.xlsx', index=False, sheet_name='IDEB')
    print("[OK] 01_dataset_ideb_processado.xlsx")
except:
    print("[AVISO] Excel nao gerado (openpyxl necessario)")

print()


# RESUMO FINAL

print("=" * 80)
print("PROCESSAMENTO CONCLUIDO COM SUCESSO!")
print("=" * 80)
print()
print("GRAFICOS GERADOS (5):")
print("  - 01_caldas_novas_ideb.png")
print("  - 02_goiania_ideb.png")
print("  - 03_comparativo_2023.png")
print("  - 04_todas_series.png")
print("  - 05_distribuicao_boxplot.png")
print()
print("DADOS EXPORTADOS:")
print("  - 01_dataset_ideb_processado.csv")
print("  - 01_dataset_ideb_processado.xlsx")
print()
print("RESUMO DOS DADOS:")
print("  Localidades: {}".format(", ".join(locais_unique)))
print("  Periodo: 2005-2023 (10 avaliacoes)")
print("  Total de registros: {}".format(len(df)))
print()
