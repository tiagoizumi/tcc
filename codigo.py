# python codigo.py > Program/runAll.sh
print("#arquivo_de_lote")
print("#!/bin/bash")
for [n, t] in [[20, 2], [25, 5], [30, 5], [40, 5], [50, 6], [60, 10], [70, 10]]:
    for d in [25, 50, 75, 100]:
        for i in range(1, 11):
            print(f'./runTest "../Instances/CKP_Classical_Instances/{d}/{i}_{n}_{d}" {t}')
