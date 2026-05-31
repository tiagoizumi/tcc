# python codigo.py > Program/runAll.sh
print("#arquivo_de_lote")
print("#!/bin/bash")
for i in range(1, 11):
    for n in [20, 25, 30, 40, 50, 60, 70]:
        for d in [25, 50, 75, 100]:
            print(f'./runTest "../Instances/CKP_Classical_Instances/{d}/{i}_{n}_{d}" 5')
