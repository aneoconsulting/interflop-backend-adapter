BACKEND_NB = 1
BACKEND_NAME = "vr_custom"
BACKEND_CALL_NAME = "custom"

BACKEND_PATH = "../backend/custom/backend.cpp"

COMPLETE_BACK_C = "../backend/custom/complete_backend.cpp"
COMPLETE_BACK_H = "../backend/custom/complete_backend.h"
TEMPLATE_BACK_C = "templates/interflop_back_code.cxx.jinja"
TEMPLATE_BACK_H = "templates/interflop_back_header.h.jinja"


VERROU_FILES = [
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/vr_main.c",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/vr_main.c",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/vr_main.h",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/vr_clo.c",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/Makefile.am",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/interflop_backends/statically_integrated_backends.h",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/generateBackendInterOperator.py",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/generateBackendInterOperator.py",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/generateBackendInterOperator.py",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/generateBackendInterOperator.py",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/generateBackendInterOperator.py",
    "verrou_repo/valgrind-3.22.0+verrou-dev/verrou/generateBackendInterOperator.py"
]

DIFF_FILES = [
    "diff_files/vr_main_c.diff",
    "diff_files/vr_main_c.diff",
    "diff_files/vr_main_h.diff",
    "diff_files/vr_clo_c.diff",
    "diff_files/makefile_am.diff",
    "diff_files/statically_integrated_backends_h.diff",
    "diff_files/generateBackendInterOperator_py.diff",
    "diff_files/generateBackendInterOperator_py.diff",
    "diff_files/generateBackendInterOperator_py.diff",
    "diff_files/generateBackendInterOperator_py.diff",
    "diff_files/generateBackendInterOperator_py.diff",
    "diff_files/generateBackendInterOperator_py.diff"
]

TEMPLATES_FILES = [
    "templates/vr_main.c1.jinja",
    "templates/vr_main.c2.jinja",
    "templates/vr_main.h.jinja",
    "templates/vr_clo.c.jinja",
    "templates/makefile.am.jinja",
    "templates/statically_integrated_backends.h.jinja",
    "templates/generateBackendInterOperator.py.jinja",
    "templates/generateBackendInterOperator.py.jinja",
    "templates/generateBackendInterOperator.py.jinja",
    "templates/generateBackendInterOperator.py.jinja",
    "templates/generateBackendInterOperator.py.jinja",
    "templates/generateBackendInterOperator.py.jinja"
]

GENERATED_HEADERS = [
    "/*---------------- GENERATED CODE FOR ADDITIONAL BACKENDS 1 -----------------*/\n",
    "/*---------------- GENERATED CODE FOR ADDITIONAL BACKENDS 2 -----------------*/\n",
    "  /* GENERATED ADDITONAL BACKEND ENUM */\n",
    "/*----------------- GENERATED CODE FOR ADDITIONAL BACKENDS ------------------*/\n",
    "##--------------- GENERATED AUTOMAKE FOR ADDITIONAL BACKENDS ----------------##\n",
    "/*----------------- GENERATED CODE FOR ADDITIONAL BACKENDS ------------------*/\n",
    "        # GENERATED ADDITIONAL BACKEND 1 #\n",
    "        # GENERATED ADDITIONAL BACKEND 2 #\n",
    "        # GENERATED ADDITIONAL BACKEND 3 #\n",
    "        # GENERATED ADDITIONAL BACKEND 4 #\n",
    "        # GENERATED ADDITIONAL BACKEND 5 #\n",
    "        # GENERATED ADDITIONAL BACKEND 6 #\n"
]

GENERATED_FOOTERS = [
    "/*------------- END OF GENERATED CODE FOR ADDITIONAL BACKENDS 1 -------------*/\n",
    "/*------------- END OF GENERATED CODE FOR ADDITIONAL BACKENDS 2 -------------*/\n",
    "  /* END OF GENERATED ADDITONAL BACKEND ENUM */\n",
    "/*-------------- END OF GENERATED CODE FOR ADDITIONAL BACKENDS --------------*/\n",
    "##------------ END OF GENERATED AUTOMAKE FOR ADDITIONAL BACKENDS ------------##\n",
    "/*-------------- END OF GENERATED CODE FOR ADDITIONAL BACKENDS --------------*/\n",
    "        # END OF GENERATED ADDITIONAL BACKEND 1 #\n",
    "        # END OF GENERATED ADDITIONAL BACKEND 2 #\n",
    "        # END OF GENERATED ADDITIONAL BACKEND 3 #\n",
    "        # END OF GENERATED ADDITIONAL BACKEND 4 #\n",
    "        # END OF GENERATED ADDITIONAL BACKEND 5 #\n",
    "        # END OF GENERATED ADDITIONAL BACKEND 6 #\n"
]

FUNCTIONS_PROTOS = [
    "void add_float(float a, float b, float *res, void *context)",
    "void sub_float(float a, float b, float *res, void *context)",
    "void mul_float(float a, float b, float *res, void *context)",
    "void div_float(float a, float b, float *res, void *context)",
    "void cmp_float(enum FCMP_PREDICATE p, float a, float b, int *res, void *context)",

    "void add_double(double a, double b, double *res, void *context)",
    "void sub_double(double a, double b, double *res, void *context)",
    "void mul_double(double a, double b, double *res, void *context)",
    "void div_double(double a, double b, double *res, void *context)",
    "void cmp_double(enum FCMP_PREDICATE p, double a, double b, int *res, void *context)"
]