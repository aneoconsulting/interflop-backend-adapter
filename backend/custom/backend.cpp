#include <stdio.h>
#include <cmath>

#include "interflop_header.hpp"

void add_float(float a, float b, float *res, void *context) noexcept {
    *res = a + b;
}

void sub_float(float a, float b, float *res, void *context) noexcept {
    *res = a - b;
}

void mul_float(float a, float b, float *res, void *context) noexcept {
    *res = a * b;
}

void div_float(float a, float b, float *res, void *context) noexcept {
    *res = a / b;
}

//void madd_float(float a, float b, float c, float c, void *context) noexcept {
//    *res = fmaf(a,b,c);
//}

void add_double(double a, double b, double *res, void *context) noexcept {
    *res = a + b;
}

void sub_double(double a, double b, double *res, void *context) noexcept {
    *res = a - b;
}

void mul_double(double a, double b, double *res, void *context) noexcept {
    *res = a * b;
}

void div_double(double a, double b, double *res, void *context) noexcept {
    *res = a / b;
}

//void madd_double(double a, double b, double *res, void *context) noexcept {
//    *res = fma(a,b,c);
//}


