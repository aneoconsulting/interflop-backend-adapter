#!/bin/python3.11

from os import listdir, makedirs
from os.path import isdir, isfile
from jinja2 import Template


BACKENDS_FOLDER_PATH = "../backend/"

COMPLETED_PATH = "completed_pene_files/"
TEMPLATE_REPLACE_MODULE = "templates/replace_module.cpp.jinja"
TEMPLATE_BACK_CODE = "templates/interflop_back_code.h.jinja"

FLOAT_TYPE = "float"
DOUBLE_TYPE = "double"

ACCEPTED_OP = [
    "add", "sub",
    "mul", "div",
    "madd", "sqrt"
]

class backend:
    """
    Class containing the backend's name and codes of each of its implemented
    functions.

    Attributes:
        name: String corresponding to name of the backend.
        op_codes: Dictionnary containing the body of each of
                  its implemented functions.

    Methods:
        _fetch_op_body: Take lines of a file and fetch the body of the asked
                        operation and type to return it at the end.
        _fetch_operations_codes: Take a backend path and go fetch each
                                 operations of each types to save their body in
                                 the "op_codes" dictionnary.
    """
    name = ""
    op_codes = {}


    def _fetch_op_body(self, lines, operation, type):
        """
        Take lines of a file and fetch the body of the asked operation and type
        to return it at the end.

        Args:
            lines: List of lines of the backend file
                   (including the new line characters).
            operation: String of the needed operation, valid ones are in the
                       ACCEPTED_OP variable.
            type: String of the needed type, can be either "float" or "double".

        Returns:
            String corresponding to the body of the operation asked.
            Empty string if not found.
        """
        body_begin = operation + "_" + type + ":"
        body_end = "end_" + operation + "_" + type

        code = ""
        read_body = False
        got_end = False

        for line in lines:
            if line.startswith(body_end):
                got_end = True
                break
            if read_body:
                code += line
            elif line.startswith(body_begin):
                read_body = True

        if got_end:
            return code
        return ""


    def _fetch_operations_codes(self, path):
        """
        Take a backend path and go fetch each operations of each types to
        save their body in the "op_codes" dictionnary.

        Args:
            path: String representing the path to the backend file.
        """
        with open(path, "r") as file:
            lines = file.readlines()

        for operation in ACCEPTED_OP:
            body = self._fetch_op_body(lines, operation, FLOAT_TYPE)
            self.op_codes[operation + "_" + FLOAT_TYPE + "_code"] = body

        for operation in ACCEPTED_OP:
            body = self._fetch_op_body(lines, operation, DOUBLE_TYPE)
            self.op_codes[operation + "_" + DOUBLE_TYPE + "_code"] = body


    def __init__(self, name, path):
        """
        Take the name and the path of the backend and save its informations
        (name and operation codes) in its own variables.

        Args:
            name: String corresponding to the name of the backend.
            path: String corresponding to the path of the backend file.
        """
        self.name = name
        self._fetch_operations_codes(path)



def complete_replace_module(backend_list):
    """
    Use backends' information in the backend class to complete the
    replace_module templates and save the completed files in the
    folder "completed_pene_files"

    Args:
        backend_list:   list of class containing the backend's name and codes of
                        each of its implemented functions
    """
    names = [backend.name for backend in backend_list]
    upper_names = [name.upper() for name in names]

    with open(TEMPLATE_REPLACE_MODULE, "r") as file:
        template = Template(file.read())

    completed_text = template.render(backend_nb=len(names),
                                     backend_names=names,
                                     upper_backend_names = upper_names)

    makedirs(COMPLETED_PATH, exist_ok=True)
    with open(COMPLETED_PATH + "replace_module.cpp", "w") as file:
        file.write(completed_text)


def get_backends_infos():
    """
    Take all the backend folders' names and functions' codes and return it as a
    list of backend class.

    Returns:
        backends_list: List of class containing the backend's name and codes of
        each of its implemented functions.
    """
    backends_list = []

    path_list = listdir(BACKENDS_FOLDER_PATH)
    for path in path_list:
        if isdir(BACKENDS_FOLDER_PATH + path):
            backends_list.append(backend(path, BACKENDS_FOLDER_PATH + path + "/backend.cpp"))

    return backends_list


def create_backend_files(backends_list):
    """
    Iterate on each backend to complete the templates of the verrou backends
    then store them in the completed files folder

    Args:
        backends_list: list of class containing the backend's name and codes of
                       each of its implemented functions
    """
    with open(TEMPLATE_BACK_CODE, "r") as file:
        template = Template(file.read())

    for backend in backends_list:
        correct_file = template.render(
            backend.op_codes,
            backend_name=backend.name,
            upper_backend_name=backend.name.upper()
        )
        with open(COMPLETED_PATH + "/complete_backend_" + backend.name + ".cpp", "w") as file:
            file.write(correct_file)


def main():
    backends_list = get_backends_infos()
    complete_replace_module(backends_list)
    create_backend_files(backends_list)


if __name__ == "__main__":
    main()
