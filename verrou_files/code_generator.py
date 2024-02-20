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

class backend:
    name = ""
    op_codes = {}

    def op_codes_list_to_dict(self, op_codes_list):
        self.op_codes["add_float"] = op_codes_list[0]
        self.op_codes["add_double"] = op_codes_list[1]
        self.op_codes["sub_float"] = op_codes_list[2]
        self.op_codes["sub_double"] = op_codes_list[3]
        self.op_codes["mul_float"] = op_codes_list[4]
        self.op_codes["mul_double"] = op_codes_list[5]
        self.op_codes["div_float"] = op_codes_list[6]
        self.op_codes["div_double"] = op_codes_list[7]
        self.op_codes["madd_float"] = op_codes_list[8]
        self.op_codes["madd_double"] = op_codes_list[9]
        self.op_codes["sqrt_float"] = op_codes_list[10]
        self.op_codes["sqrt_double"] = op_codes_list[11]


    def __init__(self, name, op_codes_list):
        self.name = name
        self.op_codes_list_to_dict(op_codes_list)



def complete_verrou_sources(backend_list):
    """
    Use the names of the backends to complete the verrou source code templates and save the completed files in the folder "completed_verrou_files"

    Args:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
    """
    names = [backend.name for backend in backend_list]
    vr_names = [("vr_" + name) for name in names]
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
    Take all the backend folders' names and path and return it as two lists

    Returns:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
        op_codes:   list of list of every fuctions' bodies to be implemented in the backend completed code
    """
    backend_list = []

    list_back = listdir(BACKENDS_FOLDER_PATH)
    for back in list_back:
        if path.isdir(BACKENDS_FOLDER_PATH + back):
            backend_list.append(backend(back, get_op_codes(BACKENDS_FOLDER_PATH + back)))

    return backend_list


def create_backend_files(backend_list):
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

    for backend in backend_list:
        correct_c = c_template.render(
            backend_name=backend.name,
            upper_backend_name=backend.name.upper(),

            add_float_code=backend.op_codes["add_float"], add_double_code=backend.op_codes["add_double"],
            sub_float_code=backend.op_codes["sub_float"], sub_double_code=backend.op_codes["sub_double"],
            mul_float_code=backend.op_codes["mul_float"], mul_double_code=backend.op_codes["mul_double"],
            div_float_code=backend.op_codes["div_float"], div_double_code=backend.op_codes["div_double"],
            madd_float_code=backend.op_codes["madd_float"], madd_double_code=backend.op_codes["madd_double"],
            sqrt_float_code=backend.op_codes["sqrt_float"], sqrt_double_code=backend.op_codes["sqrt_double"]
        )
        with open(COMPLETED_PATH + "/complete_backend_" + backend.name + ".cpp", "w") as file:
            file.write(correct_c)

        with open(TEMPLATES_PATH + TEMPLATE_BACK_H, "r") as file:
            h_template = Template(file.read())
        correct_h = h_template.render(
            backend_name=backend.name,
            upper_backend_name=backend.name.upper(),
        )
        with open(COMPLETED_PATH + "/complete_backend_" + backend.name + ".h", "w") as file:
            file.write(correct_h)


def main():
    backend_list = get_backends_infos()
    complete_verrou_sources(backend_list)
    create_backend_files(backend_list)


if __name__ == "__main__":
    main()
