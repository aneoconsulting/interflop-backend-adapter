

#include <immintrin.h>
#include <iostream>
#include <string>
#include <iomanip>

int main(){

    std::cout<< "This programme is used for tests the instrumentation of the programme with the three tools" << std::endl;

    float z = 1.0;
    float x = 0.0;

    float sum = z+x;

    std::cout << "Result :" << std::endl;
    std::cout << std::setprecision(23) << std::hexfloat << sum << std::endl;

    return 0;
}
