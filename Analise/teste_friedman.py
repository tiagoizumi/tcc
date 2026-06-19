import pandas as pd
from scipy.stats import friedmanchisquare

# Leitura

NOME_DO_ARQUIVO = "Results_TSP_RKO.csv"

print(f"1. Lendo o arquivo: {NOME_DO_ARQUIVO}...")

# Limpeza padrão
try:
    df = pd.read_csv(NOME_DO_ARQUIVO, sep=';')
except Exception as e:
    df = pd.read_excel(NOME_DO_ARQUIVO)

print(f"-> Total de linhas lidas no arquivo: {len(df)}")


df.columns = df.columns.str.strip()
df['Metaheuristica'] = df['Metaheuristica'].astype(str).str.strip()
df['Instancia'] = df['Instancia'].astype(str).str.strip()

# Identificar as meta-heurísticas presentes
metaheurísticas_unicas = list(df['Metaheuristica'].unique())
print(f"2. Meta-heurísticas identificadas para o teste: {metaheurísticas_unicas}")

# Mude para 'Melhor' se quiser testar a qualidade da solução
METRICA = 'TempoMelhor'
print(f"-> Métrica selecionada para a análise: '{METRICA}'")

try:
    matriz_dados = df.pivot(index='Instancia', columns='Metaheuristica', values=METRICA)
    matriz_dados = matriz_dados.dropna()
    print(f"-> Matriz gerada com sucesso: {matriz_dados.shape[0]} instâncias válidas pareadas.")
except Exception as e:
    print(f"Erro ao pivotar a tabela. Certifique-se de que cada algoritmo rodou exatamente as mesmas instâncias.")
    raise e


print("\n4. Executando o Teste de Friedman Global...")

dados_por_algoritmo = [matriz_dados[mh].values for mh in metaheurísticas_unicas]
stat, p_valor = friedmanchisquare(*dados_por_algoritmo)

# Determinar se a diferença global é significativa (Alfa = 5%)
significativo = "Sim" if p_valor < 0.05 else "Não"

rankings = matriz_dados.rank(axis=1, ascending=True)
rankings_medios = rankings.mean().reset_index()
rankings_medios.columns = ['Metaheuristica', 'Ranking Médio (Menor é Melhor)']
rankings_medios = rankings_medios.sort_values(by='Ranking Médio (Menor é Melhor)').reset_index(drop=True)

# Resultados
print("\n" + "="*70)
print(f"RESULTADOS DO TESTE DE FRIEDMAN PARA: {METRICA.upper()}")
print("="*70)
print(f"Estatística de Friedman (Chi-square): {stat:.4f}")
print(f"p-valor Global: {p_valor}")
print(f"Existe diferença significativa no grupo? {significativo}")
print("-" * 70)

print("\n RANKING DOS ALGORITMOS (Baseado no Teste de Friedman):")
display(rankings_medios)

resumo_friedman = pd.DataFrame([{
    'Métrica Analisada': METRICA,
    'Estatística Chi-square': stat,
    'p-valor Global': p_valor,
    'Diferença Significativa (p < 0.05)?': significativo
}])


resumo_friedman.to_csv('resultado_friedman_global.csv', index=False, sep=';', encoding='utf-8-sig')
rankings_medios.to_csv('resultado_friedman_rankings.csv', index=False, sep=';', encoding='utf-8-sig')

print("\n Relatórios exportados com sucesso:")
print("- 'resultado_friedman_global.csv' (Estatísticas globais do teste)")
print("- 'resultado_friedman_rankings.csv' (Tabela de ordens/rankings dos algoritmos)")