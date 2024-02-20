#!/bin/python3.11

from os import listdir, path
from jinja2 import Template


BACKENDS_FOLDER_PATH = "../backend/"

TEMPLATES_PATH = "templates/"
COMPLETED_PATH = "completed_verrou_files/"

TEMPLATE_BACK_C = "interflop_back_code.cxx.jinja"
TEMPLATE_BACK_H = "interflop_back_header.h.jinja"

FUNCTIONS_BEGIN = [
    "add_float:", "add_double:",
    "sub_float:", "sub_double:",
    "mul_float:", "mul_double:",
    "div_float:", "div_double:",
    "madd_float:", "madd_double:",
    "sqrt_float:", "sqrt_double:"
]


def complete_verrou_sources(names, vr_names):
    """
    Use the infos to complete the verrou source code templates and save the completed files in the folder "completed_verrou_files"

    Args:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
    """
    for template_name in listdir(TEMPLATES_PATH):
        if path.isfile(TEMPLATES_PATH + template_name) and not template_name.startswith("interflop_back"):
            with open(TEMPLATES_PATH + template_name, "r") as file:
                template = Template(file.read())
            completed_text = template.render(backend_nb=len(names),
                                        backend_vr_names=vr_names,
                                        backend_names=names)
            # template_name[:-6] to remove the .jinja at the end of the name
            with open(COMPLETED_PATH + template_name[:-6], "w") as file:
                file.write(completed_text)


def get_op_codes(path):
    """
    Take a backend formated file and return a list of the body of every disponible functions found

    Args:
        path: str representing the path to the backend folder

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


def get_backends_infos():
    """
    Take all the backend folders' names and path and return it as a dictionary containing three lists

    Returns:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
        op_codes:   list of list of every fuctions' bodies to be implemented in the backend completed code
    """
    names = []
    vr_names = []
    op_codes = []

    list_back = listdir(BACKENDS_FOLDER_PATH)
    for back in list_back:
        if path.isdir(BACKENDS_FOLDER_PATH + back):
            names.append(back)
            vr_names.append("vr_" + back)
            op_codes.append(get_op_codes(BACKENDS_FOLDER_PATH + back))

    return names, vr_names, op_codes


def create_backend_files(names, vr_names, op_codes):
    """
    Iterate on each backend's names, get their implemented functions and complete the templates of
    the verrou backends then store them completed files folder

    Args:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
        op_codes:   list of list of every fuctions' bodies to be implemented in the backend completed code
    """
    with open(TEMPLATES_PATH + TEMPLATE_BACK_C, "r") as file:
        c_template = Template(file.read())

    for i in range(len(names)):
        correct_c = c_template.render(
            backend_name=vr_names[i],
            backend_call_name=names[i],
            upper_backend_call_name=names[i].upper(),

            add_float_code=op_codes[i][0], add_double_code=op_codes[i][1],
            sub_float_code=op_codes[i][2], sub_double_code=op_codes[i][3],
            mul_float_code=op_codes[i][4], mul_double_code=op_codes[i][5],
            div_float_code=op_codes[i][6], div_double_code=op_codes[i][7],

            madd_float_code=op_codes[i][8], madd_double_code=op_codes[i][9],
            sqrt_float_code=op_codes[i][10], sqrt_double_code=op_codes[i][11]
        )
        with open(COMPLETED_PATH + "/complete_backend.cpp", "w") as file:
            file.write(correct_c)

        with open(TEMPLATES_PATH + TEMPLATE_BACK_H, "r") as file:
            h_template = Template(file.read())
        correct_h = h_template.render(
            backend_name=vr_names[i],
            backend_call_name=names[i],
            upper_backend_call_name=names[i].upper()
        )
        with open(COMPLETED_PATH + "/complete_backend.h", "w") as file:
            file.write(correct_h)


def main():
    names, vr_names, op_codes = get_backends_infos()
    complete_verrou_sources(names, vr_names)
    create_backend_files(names, vr_names, op_codes)


if __name__ == "__main__":
    main()
