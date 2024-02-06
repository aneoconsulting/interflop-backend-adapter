#include <stdio.h>
#include <cmath>

#include "interflop_header.hpp"

void add_float(float a, float b, float* cptr, void*) noexcept {
    *cptr = a + b;
}

void sub_float(float a, float b, float* cptr, void*) noexcept {
    *cptr = a - b;
}

void mul_float(float a, float b, float* cptr, void*) noexcept {
    *cptr = a * b;
}

void div_float(float a, float b, float* cptr, void*) noexcept {
    *cptr = a / b;
}

//void madd_float(float a, float b, float c, float* cptr, void*) noexcept {
//    *cptr = fmaf(a,b,c);
//}

void add_double(double a, double b, double* cptr, void*) noexcept {
    *cptr = a + b;
}

void sub_double(double a, double b, double* cptr, void*) noexcept {
    *cptr = a - b;
}

void mul_double(double a, double b, double* cptr, void*) noexcept {
    *cptr = a * b;
}

void div_double(double a, double b, double* cptr, void*) noexcept {
    *cptr = a / b;
}

//void madd_double(double a, double b, double c, double* cptr, void*) noexcept {
//    *cptr = fma(a,b,c);
//}


