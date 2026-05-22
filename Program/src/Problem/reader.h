#ifndef READER_H
#define READER_H

#include <vector>
#include <string>

using Vector   = std::vector<double>;
using Matrix2D = std::vector<std::vector<double>>;
using Matrix3D = std::vector<std::vector<std::vector<double>>>;

struct CKPInstance {
    Vector C;
    Matrix2D P;
    Matrix3D D;
    Vector W;
    double B;
};

CKPInstance carregarInstancia(int i, int n, int d);

#endif