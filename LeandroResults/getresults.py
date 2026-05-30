def f_obj(i, n, d, sol):
    # Ler os arquivos
    ## Benefícios lineares (C)
    with open(f'../Instances/CKP_Classical_instances/{d}/C_{i}_{n}_{d}.txt') as f:
        C = list(map(int, f.read().split()))
    ## Benefícios quadráticos (P)
    with open(f'../Instances/CKP_Classical_instances/{d}/P_{i}_{n}_{d}.txt') as f:
        valores_p = list(map(int, f.read().split()))
        P = []
        for idx in range(0, len(valores_p), n):
            P.append(valores_p[idx : idx + n])
    ## Benefícios cúbicos (D)
    with open(f'../Instances/CKP_Classical_instances/{d}/D_{i}_{n}_{d}.txt') as f:
        valores_d = list(map(int, f.read().split()))
        # Reconstrói o cubo n x n x n
        D = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
        idx = 0
        for x in range(n):
            for j in range(n):
                for k in range(n):
                    D[x][j][k] = valores_d[idx]
                    idx += 1

    tot = 0 # Cálculo FO
    for x in range(n): # Linear
        tot += C[x] * sol[x]
    for x in range(n): # Quadrática
        for j in range(n):
            tot += P[x][j] * sol[x] * sol[j]
    for x in range(n): # Cúbica
        for j in range(n):
            for k in range(n):
                tot += D[x][j][k] * sol[x] * sol[j] * sol[k]

    return tot

# Únicos disponíveis
I = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
N = [20, 25, 30, 40]
D = [25, 50, 75, 100]

i = 1
n = 20
d = 25
exact = list()

for i in I:
    for n in N:
        for d in D:
            exact = list()
            with open(f'Exact_Solution_CI/{d}/Exact_Solution_{n}.txt', 'r', encoding='utf-8') as arquivo:
                for idx, linha in enumerate(arquivo):
                    exact.append(list(map(int, linha.strip().replace('Exact: ', '').split(' '))))
            print(f'{i}, {n}, {d}, {f_obj(i, n, d, exact[i-1])}')

