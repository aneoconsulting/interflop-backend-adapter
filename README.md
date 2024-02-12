# backend-adapter
Take an interflop backend and port it to PENE, Verrou and Verificarlo

## Function declaration

the "backend.cpp" should begin the declaration lines of the functions like this:

- void add_float(float a, float b, float *res, void *context)
- void sub_float(float a, float b, float *res, void *context)
- void mul_float(float a, float b, float *res, void *context)
- void div_float(float a, float b, float *res, void *context)
- void cmp_float(enum FCMP_PREDICATE p, float a, float b, int *res, void *context)

- void add_double(double a, double b, double *res, void *context)
- void sub_double(double a, double b, double *res, void *context)
- void mul_double(double a, double b, double *res, void *context)
- void div_double(double a, double b, double *res, void *context)
- void cmp_double(enum FCMP_PREDICATE p, double a, double b, int *res, void *context)

It will use this to recognize the functions and their position in the code to adapt them to the front-end used.

Don't bother using keywords like "noexcept" or anything else after the function declaration, only the body of the function matter, the rest won't be used (at least for now).