

static void add_float(float a, float b, float* cptr, void*) noexcept;
static void sub_float(float a, float b, float* cptr, void*) noexcept;
static void mul_float(float a, float b, float* cptr, void*) noexcept;
static void div_float(float a, float b, float* cptr, void*) noexcept;
static void madd_float(float a, float b, float c, float* cptr, void*) noexcept;

static void add_double(double a, double b, double* cptr, void*) noexcept;
static void sub_double(double a, double b, double* cptr, void*) noexcept;
static void mul_double(double a, double b, double* cptr, void*) noexcept;
static void div_double(double a, double b, double* cptr, void*) noexcept;
static void madd_double(double a, double b, double c, double* cptr, void*) noexcept;
static void* init() noexcept { return nullptr; };
/*--- PENE exclusive ---*/
static void madd_float(float a, float b, float c, float* cptr, void*) noexcept;
/*----------------------*/

static void add_double(double a, double b, double* cptr, void*) noexcept;
static void sub_double(double a, double b, double* cptr, void*) noexcept;
static void mul_double(double a, double b, double* cptr, void*) noexcept;
static void div_double(double a, double b, double* cptr, void*) noexcept;
/*--- PENE exclusive ---*/
static void madd_double(double a, double b, double c, double* cptr, void*) noexcept;
