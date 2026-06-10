// C++ library
#include <sys/time.h>
#include <math.h>
#include <cstring>
#include <ctime>
#include <iostream>
// Windows
#if defined(_WIN32) || defined(_WIN64)  
    #include <windows.h>
// Unix-like (Linux, macOS)
#else  
    #include <time.h>
#endif
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <string.h>
#include <algorithm>
#include <utility>  
#include <numeric>  
#include <map>
#include <limits>
#include <random>
#include <chrono>
#include <iomanip> 
#include <sstream> 
#include <fstream> 
#include <omp.h>
#include <atomic>

#include "../Program/src/Data.h"
#include "../Program/src/Problem/Problem.h"


int main() {
    TProblemData data;
    TSol s;
    char name[100] = "../Instances/CKP_Classical_Instances/25/8_20_25";
    double res;

    s.rk = {0.523, 0.920, 0.772, 0.443, 0.499, 0.769, 0.057, 0.784, 0.789, 0.960, 0.749, 0.846, 0.970, 0.989, 0.535, 0.863, 0.760, 0.938, 0.870, 0.862};
    ReadData(name, data);
    res = Decoder(s, data);
    printf("OFV: %.5lf\n", res);
}
