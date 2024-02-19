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

FUNCTIONS_BEGIN = [
    "add_float:", "add_double:",
    "sub_float:", "sub_double:",
    "mul_float:", "mul_double:",
    "div_float:", "div_double:",
    "madd_float:", "madd_double:",
    "sqrt_float:", "sqrt_double:"
]

TEMPLATE_BACK_C = "templates/interflop_back_code.c.jinja"


def get_backends_paths():
    """
    Take all the backend folders' paths and return it as a list

    Returns:
        paths:    list of all the relative paths of every backend folders
    """
    paths = []

    list_back = listdir(BACKENDS_FOLDER_PATH)
    for back in list_back:
        if path.isdir(BACKENDS_FOLDER_PATH + back):
            paths.append(BACKENDS_FOLDER_PATH + back)

    return paths


def get_op_codes(path):
    """
    Take a backend formated file and return a list of the body of every disponible functions found

    Args:
        path: str representing the path to the backend file

    Returns:
        List of the body of every functions named in FUNCTION_BEGIN, "" if the function is not found
    """
    op_codes = []

    with open(path + "/backend.cpp", "r") as file:
        lines = file.readlines()

    for begin in FUNCTIONS_BEGIN:
        code = ""
        read_body = False
        got_end = False

        for line in lines:
            if line.startswith("end_" + begin[:-1]):
                got_end = True
                break
            if read_body:
                code += line
            elif line.startswith(begin):
                read_body = True

        if got_end:
            op_codes.append(code)
        else:
            op_codes.append("")

    return op_codes


def create_backend_files(backends_paths):
    """
    Iterate on each backend's names, get their implemented functions and complete the templates of
    the verrou backends then store them in the backend respective folder

    Args:
        backends_paths: list of all the relative paths of every backend folders
    """
    with open(TEMPLATE_BACK_C, "r") as file:
        c_template = Template(file.read())

    for path in backends_paths:
        op_codes = get_op_codes(path)

        correct_c = c_template.render(
            add_float_code=op_codes[0], add_double_code=op_codes[1],
            sub_float_code=op_codes[2], sub_double_code=op_codes[3],
            mul_float_code=op_codes[4], mul_double_code=op_codes[5],
            div_float_code=op_codes[6], div_double_code=op_codes[7],
            madd_float_code=op_codes[8], madd_double_code=op_codes[9],
            sqrt_float_code=op_codes[10], sqrt_double_code=op_codes[11]
        )

        with open(path + "/complete_backend.cpp", "w") as file:
            file.write(correct_c)


def main():
    backends_paths = get_backends_paths()
    create_backend_files(backends_paths)


if __name__ == "__main__":
    main()