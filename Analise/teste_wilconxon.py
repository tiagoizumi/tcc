import pandas as pd
from scipy.stats import wilcoxon

# Leitura
NOME_DO_ARQUIVO = "Results_TSP_RKO.csv"

try:
    df = pd.read_csv(NOME_DO_ARQUIVO, sep=';')
except Exception as e:
    df = pd.read_excel(NOME_DO_ARQUIVO)

# Limpeza padrão
df.columns = df.columns.str.strip()
df['Metaheuristica'] = df['Metaheuristica'].astype(str).str.strip()
df['Instancia'] = df['Instancia'].astype(str).str.strip()

metaheurísticas_unicas = df['Metaheuristica'].unique()

# Separar a metaheuristica alvo da comparacao (SA)
nome_sa = metaheurísticas_unicas[0]
dados_sa = df[df['Metaheuristica'] == nome_sa].sort_values(by='Instancia')

resultados_tempo_avancado = []

for mh in metaheurísticas_unicas[1:]:
    dados_outro = df[df['Metaheuristica'] == mh].sort_values(by='Instancia')

    if len(dados_sa) != len(dados_outro):
        continue

    tempos_sa = dados_sa['TempoMelhor'].values
    tempos_outro = dados_outro['TempoMelhor'].values

    media_sa = tempos_sa.mean()
    media_outro = tempos_outro.mean()

    # Teste Bicaudal
    try:
        _, p_bicaudal = wilcoxon(tempos_sa, tempos_outro, alternative='two-sided')
    except ValueError:
        p_bicaudal = 1.0

    # Se for significativo, descobrimos a direção estatística
    if p_bicaudal < 0.05:
        significativo = "Sim"

        # Testando se a metaheuristica é mais lenta (Tempo MH > Tempo Outro)
        _, p_greater = wilcoxon(tempos_sa, tempos_outro, alternative='greater')

        # Testando se a metaheuristica é mais rapida (Tempo MH < Tempo Outro)
        _, p_less = wilcoxon(tempos_sa, tempos_outro, alternative='less')

        # Interpretando os p-valores unilaterais
        if p_greater < 0.05:
            veredito = f"{mh} é estatisticamente MAIS RÁPIDO que {nome_sa}"
            p_unilateral = p_greater
        elif p_less < 0.05:
            veredito = f"{nome_sa} é estatisticamente MAIS RÁPIDO que {mh}"
            p_unilateral = p_less
        else:
            veredito = "Diferença inconclusiva na direção"
            p_unilateral = min(p_greater, p_less)
    else:
        significativo = "Não"
        veredito = "Algoritmos Equivalentes (Empate)"
        p_unilateral = "N/A"

    resultados_tempo_avancado.append({
        'Comparação': f"{nome_sa} vs {mh}",
        f'Média {nome_sa}': media_sa,
        f'Média {mh}': media_outro,
        'Significativo (Bicaudal)?': significativo,
        'p-valor (Bicaudal)': p_bicaudal,
        'p-valor (Unilateral)': p_unilateral,
        'Veredito Final': veredito
    })


# Resultados
df_final = pd.DataFrame(resultados_tempo_avancado)
print("\n" + "="*75 + "\nANÁLISE DIRECIONAL DE TEMPO (WILCOXON UNILATERAL)\n" + "="*75)
display(df_final)


df_final.to_csv('Wilcoxon_direcional_tempo.csv', index=False, sep=';', encoding='utf-8-sig')