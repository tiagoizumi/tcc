#ifndef _PROBLEM_H
#define _PROBLEM_H

struct TProblemData
{
    int n;       // size of the RKO vector (= nItems)
    int nItems;
    int cap;
    std::vector<int> w;                           // weights
    std::vector<int> c;                           // linear benefits
    std::vector<std::vector<int>> p;              // quadratic benefits
    std::vector<std::vector<std::vector<int>>> d; // cubic benefits
};

void ReadData(char name[], TProblemData &data)
{
    // name é o caminho da pasta + prefixo da instância
    // ex: "../Instances/CKP_Classical_Instances/25/1_20_25"
    std::string base(name);

    // Extrai o diretório e o sufixo (ex: "1_20_25")
    size_t lastSlash = base.find_last_of("/\\");
    std::string dir    = base.substr(0, lastSlash + 1); // "../.../25/"
    std::string suffix = base.substr(lastSlash + 1);    // "1_20_25"

    auto openFile = [](const std::string &path) -> FILE* {
        FILE *f = fopen(path.c_str(), "r");
        if (!f) {
            printf("\nERROR: File (%s) not found!\n", path.c_str());
            exit(1);
        }
        return f;
    };

    // Monta caminhos no padrão: B_1_20_25.txt
    std::string pathB = dir + "B_" + suffix + ".txt";
    std::string pathW = dir + "W_" + suffix + ".txt";
    std::string pathC = dir + "C_" + suffix + ".txt";
    std::string pathP = dir + "P_" + suffix + ".txt";
    std::string pathD = dir + "D_" + suffix + ".txt";

    // --- Read B (capacity) ---
    FILE *fB = openFile(pathB);
    fscanf(fB, "%d", &data.cap);
    fclose(fB);

    // --- Read W (weights) ---
    FILE *fW = openFile(pathW);
    data.w.clear();
    int val;
    while (fscanf(fW, "%d", &val) == 1)
        data.w.push_back(val);
    fclose(fW);

    data.nItems = data.w.size();
    data.n = data.nItems;
    int n = data.n;

    // --- Read C (linear benefits) ---
    FILE *fC = openFile(pathC);
    data.c.resize(n);
    for (int i = 0; i < n; i++)
        fscanf(fC, "%d", &data.c[i]);
    fclose(fC);

    // --- Read P (quadratic benefits) ---
    FILE *fP = openFile(pathP);
    data.p.assign(n, std::vector<int>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            fscanf(fP, "%d", &data.p[i][j]);
    fclose(fP);

    // --- Read D (cubic benefits) ---
    FILE *fD = openFile(pathD);
    data.d.assign(n, std::vector<std::vector<int>>(n, std::vector<int>(n, 0)));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                fscanf(fD, "%d", &data.d[i][j][k]);
    fclose(fD);
}

// Básico 
double Decoder1(TSol &s, const TProblemData &data)
{
    int n = data.n;
    std::vector<int> x(n, 0);
    for (int i = 0; i < n; i++)
    if (s.rk[i] > 0.5)
    x[i] = 1;
    // std::vector<int> x = {0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1};

    // Check capacity
    int totalW = 0;
    for (int i = 0; i < n; i++)
        totalW += data.w[i] * x[i];

    int infeasible = std::max(0, totalW - data.cap);

    // Objective: linear + quadratic + cubic terms
    double cost = 0.0;

    // Linear
    for (int i = 0; i < n; i++)
        cost += data.c[i] * x[i];

    // Quadratic (i < j to avoid double counting)
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (i != j)
                cost += data.p[i][j] * x[i] * x[j];

    // Cubic (i < j < k)
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                if (i != j && j != k && i != k)
                    cost += data.d[i][j][k] * x[i] * x[j] * x[k];

    // Penalty for infeasibility
    cost -= 100000.0 * infeasible;

    // Minimization
    return -cost;
}

// Incremental
double Decoder(TSol &s, const TProblemData &data)
{
    int n = data.nItems;

    std::vector<int> order(n);
    for (int i = 0; i < n; i++)
        order[i] = i;

    std::sort(order.begin(), order.end(),
        [&](int a, int b) {
            return s.rk[a] > s.rk[b];
        });

    std::vector<int> x(n, 0); // vetor binário
    double weight = 0.0;

    for (int idx = 0; idx < n; idx++)
    {
        int i = order[idx];

        if (weight + data.w[i] <= data.cap)
        {
            x[i] = 1;
            weight += data.w[i];
        }
    }

    ////////// VERIFY
    for (int x : x) {
        std::cout << x << " ";
    }
    printf("\nPeso total: %d (capacidade: %d)\n", (int)weight, data.cap);

    double cost = 0.0;

    // Linear
    for (int i = 0; i < n; i++)
        cost += data.c[i] * x[i];

    // Quadratic (i < j to avoid double counting)
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (i != j)
                cost += data.p[i][j] * x[i] * x[j];

    // Cubic (i < j < k)
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                if (j != k && i != k)
                    cost += data.d[i][j][k] * x[i] * x[j] * x[k];

    return -cost;
}

void FreeMemoryProblem(TProblemData &data)
{
    data.c.clear();
    data.w.clear();
    data.p.clear();
    data.d.clear();
}

#endif