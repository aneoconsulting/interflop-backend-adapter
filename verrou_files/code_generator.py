#!/bin/python3.11

from os import listdir, path
from jinja2 import Template


BACKENDS_FOLDER_PATH = "../backend/"

TEMPLATES_PATH = "templates/"
COMPLETED_PATH = "completed_verrou_files/"


def complete_verrou_sources(names, vr_names):
    """
    Use the names of the backends to complete the verrou source code templates and save the completed files in the folder "completed_verrou_files"

    Args:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
    """
    for template_name in listdir(TEMPLATES_PATH):
        if path.isfile(TEMPLATES_PATH + template_name) and template_name.endswith(".jinja"):
            with open(TEMPLATES_PATH + template_name, "r") as file:
                template = Template(file.read())
            completed_text = template.render(backend_nb=len(names),
                                        backend_vr_names=vr_names,
                                        backend_names=names)
            with open(COMPLETED_PATH + template_name[:-6], "w") as file:
                file.write(completed_text)


def get_backends_infos():
    """
    Take all the backend folders' names and path and return it as two lists

    Returns:
        names:      list of names of every backend folder
        vr_names:   same as the names list but with the string "vr_" at the beginning of each element
    """
    names = []
    vr_names = []

    list_back = listdir(BACKENDS_FOLDER_PATH)
    for back in list_back:
        if path.isdir(BACKENDS_FOLDER_PATH + back):
            names.append(back)
            vr_names.append("vr_" + back)

    return names, vr_names


def main():
    names, vr_names, paths = get_backends_infos()
    complete_verrou_sources(names, vr_names, paths)


if __name__ == "__main__":
    main()
