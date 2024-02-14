#!/bin/python3.11

from os import listdir, path
from jinja2 import Template


BACKENDS_FOLDER_PATH = "../backend/"

TEMPLATES_PATH = "templates/"
COMPLETED_PATH = "completed_verrou_files/"

VERROU_SOURCE_NAMES = [
    "vr_main.c",
    "vr_main.h",
    "vr_clo.c",
    "makefile.am",
    "statically_integrated_backends.h",
    "generateBackendInterOperator.py"
]

FUNCTIONS_PROTOS = [
    "void add_float(float a, float b, float *res, void *context)",
    "void sub_float(float a, float b, float *res, void *context)",
    "void mul_float(float a, float b, float *res, void *context)",
    "void div_float(float a, float b, float *res, void *context)",
    "void madd_float(float a, float b, float c, float *res, void *context)",
    "void sqrt_float(float a, float *res, void *context)",

    "void add_double(double a, double b, double *res, void *context)",
    "void sub_double(double a, double b, double *res, void *context)",
    "void mul_double(double a, double b, double *res, void *context)",
    "void div_double(double a, double b, double *res, void *context)",
    "void madd_double(double a, double b, double c, double *res, void *context)",
    "void sqrt_double(double a, double *res, void *context)",
]

TEMPLATE_BACK_C = "templates/interflop_back_code.cxx.jinja"
TEMPLATE_BACK_H = "templates/interflop_back_header.h.jinja"


def complete_verrou_sources(backends_infos):
    for name in VERROU_SOURCE_NAMES:
        with open(TEMPLATES_PATH + name + ".jinja", "r") as file:
            template = Template(file.read())
        completed_text = template.render(backend_nb=len(backends_infos["names"]),
                                       backend_vr_names=backends_infos["vr_names"],
                                       backend_names=backends_infos["names"])
        with open(COMPLETED_PATH + name, "w") as file:
            file.write(completed_text)


def get_backends_infos():
    backends_infos = {
                        "names": [],
                        "vr_names": [],
                        "paths": []
                    }

    list_back = listdir(BACKENDS_FOLDER_PATH)
    for back in list_back:
        if path.isdir(BACKENDS_FOLDER_PATH + back):
            backends_infos["names"].append(back)
            backends_infos["vr_names"].append("vr_" + back)
            backends_infos["paths"].append(BACKENDS_FOLDER_PATH + back)

    return backends_infos


def get_op_codes(path):
    op_codes = []

    with open(path + "/backend.cpp", "r") as file:
        lines = file.readlines()

    for proto in FUNCTIONS_PROTOS:
        code = ""
        brackets_count = 0
        begin_line = 0

        while begin_line < len(lines) and not lines[begin_line].startswith(proto):
            begin_line += 1
        if begin_line < len(lines):
            while (first_brack := lines[begin_line].find("{")) < 0:
                begin_line += 1
                if begin_line >= len(lines):
                    return []
            end_line = begin_line
            brackets_count += lines[end_line].count("{")
            brackets_count -= lines[end_line].count("}")
            while brackets_count > 0:
                end_line += 1
                if end_line >= len(lines):
                    return []
                brackets_count += lines[end_line].count("{")
                brackets_count -= lines[end_line].count("}")

            if brackets_count < 0:
                return []
            last_bracket = lines[end_line].rfind("}")
            if begin_line == end_line:
                code += lines[begin_line][first_brack+1:last_bracket-2]
            else:
                code += lines[begin_line][first_brack+1:]
                for i in range(begin_line+1, end_line):
                    code += lines[i]
                code += lines[end_line][:last_bracket-2]

            op_codes.append(code)
        else:
            op_codes.append("")

    return op_codes


def create_backend_files(backends_infos):
    with open(TEMPLATE_BACK_C, "r") as file:
        c_template = Template(file.read())

    for i in range(len(backends_infos["names"])):
        op_codes = get_op_codes(backends_infos["paths"][i])

        correct_c = c_template.render(
            backend_name=backends_infos["vr_names"][i],
            backend_call_name=backends_infos["names"][i],
            upper_backend_call_name=backends_infos["names"][i].upper(),
            add_float_code=op_codes[0],
            sub_float_code=op_codes[1],
            mul_float_code=op_codes[2],
            div_float_code=op_codes[3],
            madd_float_code=op_codes[4],
            sqrt_float_code=op_codes[5],

            add_double_code=op_codes[6],
            sub_double_code=op_codes[7],
            mul_double_code=op_codes[8],
            div_double_code=op_codes[9],
            madd_double_code=op_codes[10],
            sqrt_double_code=op_codes[11]
        )
        with open(backends_infos["paths"][i] + "/complete_backend.cpp", "w") as file:
            file.write(correct_c)

        with open(TEMPLATE_BACK_H, "r") as file:
            h_template = Template(file.read())
        correct_h = h_template.render(
            backend_name=backends_infos["vr_names"][i],
            backend_call_name=backends_infos["names"][i],
            upper_backend_call_name=backends_infos["names"][i].upper()
        )

        with open(backends_infos["paths"][i] + "/complete_backend.h", "w") as file:
            file.write(correct_h)


def main():
    backends_infos = get_backends_infos()
    complete_verrou_sources(backends_infos)
    create_backend_files(backends_infos)


if __name__ == "__main__":
    main()
