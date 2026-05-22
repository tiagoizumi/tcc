#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include "reader.h"

// ===================== Tipos =====================

using Vector   = std::vector<double>;
using Matrix2D = std::vector<std::vector<double>>;
using Matrix3D = std::vector<std::vector<std::vector<double>>>;


// ===================== Funções auxiliares =====================

Vector lerVetor(const std::string& caminho, size_t n) {
    std::ifstream arq(caminho);
    if (!arq)
        throw std::runtime_error("Erro ao abrir arquivo: " + caminho);

    Vector v(n);
    for (size_t i = 0; i < n; ++i) {
        if (!(arq >> v[i]))
            throw std::runtime_error("Erro ao ler vetor em: " + caminho);
    }

    return v;
}

Matrix2D lerMatriz2D(const std::string& caminho, size_t n) {
    std::ifstream arq(caminho);
    if (!arq)
        throw std::runtime_error("Erro ao abrir arquivo: " + caminho);

    Matrix2D m(n, std::vector<double>(n));

    for (size_t i = 0; i < n; ++i)
        for (size_t j = 0; j < n; ++j)
            if (!(arq >> m[i][j]))
                throw std::runtime_error("Erro ao ler matriz 2D em: " + caminho);

    return m;
}

Matrix3D lerMatriz3D(const std::string& caminho, size_t n) {
    std::ifstream arq(caminho);
    if (!arq)
        throw std::runtime_error("Erro ao abrir arquivo: " + caminho);

    Matrix3D m(
        n,
        std::vector<std::vector<double>>(
            n,
            std::vector<double>(n)
        )
    );

    for (size_t i = 0; i < n; ++i)
        for (size_t j = 0; j < n; ++j)
            for (size_t k = 0; k < n; ++k)
                if (!(arq >> m[i][j][k]))
                    throw std::runtime_error("Erro ao ler matriz 3D em: " + caminho);

    return m;
}

double lerEscalar(const std::string& caminho) {
    std::ifstream arq(caminho);
    if (!arq)
        throw std::runtime_error("Erro ao abrir arquivo: " + caminho);

    double valor;
    if (!(arq >> valor))
        throw std::runtime_error("Erro ao ler escalar em: " + caminho);

    return valor;
}

// ===================== Função principal solicitada =====================

CKPInstance carregarInstancia(int i, int n, int d) {

    std::string pasta =
        "CKP_Classical_Instances/" + std::to_string(d) + "/";

    std::string sufixo =
        "_" + std::to_string(i) +
        "_" + std::to_string(n) +
        "_" + std::to_string(d) + ".txt";

    CKPInstance inst;

    inst.C = lerVetor(pasta + "C" + sufixo, n);
    inst.P = lerMatriz2D(pasta + "P" + sufixo, n);
    inst.D = lerMatriz3D(pasta + "D" + sufixo, n);
    inst.W = lerVetor(pasta + "W" + sufixo, n);
    inst.B = lerEscalar(pasta + "B" + sufixo);

    return inst;
}

// ===================== Main de teste =====================

int main() {

    try {
        int i = 1;
        int n = 20;
        int d = 25;

        CKPInstance inst = carregarInstancia(i, n, d);

        std::cout << "Instância carregada com sucesso.\n";
        std::cout << "Capacidade B: " << inst.B << "\n";
        std::cout << "C[0]: " << inst.C[0] << "\n";
        std::cout << "P[0][1]: " << inst.P[0][1] << "\n";
        std::cout << "D[0][1][2]: " << inst.D[0][1][2] << "\n";
    }
    catch (const std::exception& e) {
        std::cerr << "Erro: " << e.what() << "\n";
        return 1;
    }

    return 0;
}