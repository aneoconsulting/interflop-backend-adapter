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

TEMPLATE_BACK_C = "templates/interflop_back_code.cxx.jinja"
TEMPLATE_BACK_H = "templates/interflop_back_header.h.jinja"


def complete_verrou_sources(backends_infos):
    """
    Use the infos to complete the verrou source code templates and save the completed files in the folder "completed_verrou_files"

    Args:
        backends_infos: dictionary of three lists:
            - "names":      the names of every backend folder
            - "vr_names":   same as "names" but with the string "vr_" at the beginning of each element
            - "paths":      the relative path of every backend folder
    """
    for name in VERROU_SOURCE_NAMES:
        with open(TEMPLATES_PATH + name + ".jinja", "r") as file:
            template = Template(file.read())
        completed_text = template.render(backend_nb=len(backends_infos["names"]),
                                       backend_vr_names=backends_infos["vr_names"],
                                       backend_names=backends_infos["names"])
        with open(COMPLETED_PATH + name, "w") as file:
            file.write(completed_text)


def get_backends_infos():
    """
    Take all the backend folders' names and path and return it as a dictionary containing three lists

    Returns:
        dictionary of three lists:
            - "names":      the names of every backend folder
            - "vr_names":   same as "names" but with the string "vr_" at the beginning of each element
            - "paths":      the relative path of every backend folder
    """
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
            print(line, end='')
            if line.startswith("end_" + begin[:-1]):
                got_end = True
                break
            if read_body:
                code += line
            elif line.startswith(begin):
                print("YES")
                read_body = True

        print("CODE = -" + code + "-")
        if got_end:
            op_codes.append(code)
        else:
            op_codes.append("")

    return op_codes


def create_backend_files(backends_infos):
    """
    Iterate on each backend's names, get their implemented functions and complete the templates of
    the verrou backends then store them in the backend respective folder

    Args:
        backends_infos: dictionary of three lists:
            - "names":      the names of every backend folder
            - "vr_names":   same as "names" but with the string "vr_" at the beginning of each element
            - "paths":      the relative path of every backend folder
    """
    with open(TEMPLATE_BACK_C, "r") as file:
        c_template = Template(file.read())

    for i in range(len(backends_infos["names"])):
        op_codes = get_op_codes(backends_infos["paths"][i])

        correct_c = c_template.render(
            backend_name=backends_infos["vr_names"][i],
            backend_call_name=backends_infos["names"][i],
            upper_backend_call_name=backends_infos["names"][i].upper(),

            add_float_code=op_codes[0], add_double_code=op_codes[1],
            sub_float_code=op_codes[2], sub_double_code=op_codes[3],
            mul_float_code=op_codes[4], mul_double_code=op_codes[5],
            div_float_code=op_codes[6], div_double_code=op_codes[7],

            madd_float_code=op_codes[8], madd_double_code=op_codes[9],
            sqrt_float_code=op_codes[10], sqrt_double_code=op_codes[11]
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
