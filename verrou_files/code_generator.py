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


def main():
    backends_infos = get_backends_infos()
    complete_verrou_sources(backends_infos)


if __name__ == "__main__":
    main()
