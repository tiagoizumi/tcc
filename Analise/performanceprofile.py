import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

def plot_performance_profile(data, title_metric):
    data = data.apply(pd.to_numeric, errors='coerce')
    data.fillna(np.inf, inplace=True)
    min_values = data.min(axis=1)
    r = data.divide(min_values, axis=0)

    plt.figure(figsize=(11, 6))
    n_instances = len(data)

    max_tau = r.replace(np.inf, np.nan).max().max()
    if np.isnan(max_tau) or max_tau == 1.0:
        max_tau = 2.0

    taus = np.linspace(1, max_tau, 1000)


    for col in data.columns:
        y = [sum(r[col] <= t) / n_instances for t in taus]
        plt.step(taus, y, label=col, where='post', lw=2.5)

    plt.xscale('log', base=2)

    plt.xlabel(r'Razão de Desempenho $\tau$ (Escala Logarítmica na Base 2)', fontsize=12)
    plt.ylabel('Fração de Instâncias Resolvidas', fontsize=12)
    plt.title(f'Performance Profile - Métrica: {title_metric}', fontsize=14, fontweight='bold', pad=15)
    plt.grid(True, which="both", ls="--", alpha=0.5)


    plt.legend(loc='lower right', fontsize=10, frameon=True, facecolor='white', edgecolor='gray')
    plt.ylim(0, 1.05)
    plt.tight_layout()
    plt.show()

# Leitura
NOME_DO_ARQUIVO = "Results_TSP_RKO.csv"

print(f"Lendo o arquivo real: {NOME_DO_ARQUIVO}...")
try:
    df_real = pd.read_csv(NOME_DO_ARQUIVO, sep=';')
except Exception as e:
    df_real = pd.read_excel(NOME_DO_ARQUIVO)

# Limpeza padrão
df_real.columns = df_real.columns.str.strip()
df_real['Metaheuristica'] = df_real['Metaheuristica'].astype(str).str.strip()
df_real['Instancia'] = df_real['Instancia'].astype(str).str.strip()

# Selecao da métrica (Tempo para a melhor solucao)
METRICA = 'TempoMelhor'


try:
    matriz_perf = df_real.pivot(index='Instancia', columns='Metaheuristica', values=METRICA)
    print(f"-> Matriz gerada com sucesso! Formato: {matriz_perf.shape[0]} instâncias x {matriz_perf.shape[1]} algoritmos.")
except Exception as e:
    print(" Erro ao pivotar. Verifique se existem instâncias duplicadas para o mesmo algoritmo.")
    raise e

plot_performance_profile(matriz_perf, title_metric=METRICA)