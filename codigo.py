for i in range(1, 11):
    for j in [20, 25, 30, 40]:
        for k in [25, 50, 75, 100]:
            print(f'./runTest "../Instances/CKP_Classical_Instances/{k}/{i}_{j}_{k}" 5')
