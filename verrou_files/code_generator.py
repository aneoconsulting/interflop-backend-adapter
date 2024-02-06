#!/bin/python3.11

from patch import fromfile
from jinja2 import Template


BACKEND_ND = 1
BACKEND_NAME = "vr_custom"
BACKEND_CALL_NAME = "custom"

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


def patch_file(diff_path):
    patch = fromfile(diff_path)
    patch.apply()


def remove_prev_gen_code(lines, head_line, index):
    while lines[head_line] != GENERATED_FOOTERS[index]:
        del lines[head_line]

    return lines


def add_template_lines(header_line, lines, template_path):
    with open(template_path, "r") as file:
        template = Template(file.read())
    correct_text = template.render(backend_nb=BACKEND_ND, backend_names=[BACKEND_NAME], backend_call_names=[BACKEND_CALL_NAME])
    correct_lines = correct_text.splitlines(keepends=True)

    lines_applied = lines[:header_line] + correct_lines + lines[header_line:]

    return lines_applied


def main():
    for i in range(len(VERROU_FILES)):
        with open(VERROU_FILES[i], "r") as file:

            if GENERATED_HEADERS[i] not in file:
                patch_file(DIFF_FILES[i])
                with open(VERROU_FILES[i], "r") as refreshed_file:
                    lines = refreshed_file.readlines()
                header_line = lines.index(GENERATED_HEADERS[i])
            else:
                with open(VERROU_FILES[i], "r") as refreshed_file:
                    lines = refreshed_file.readlines()
                header_line = lines.index(GENERATED_HEADERS[i]) + 1
                lines = remove_prev_gen_code(lines, header_line, i)

        lines = add_template_lines(header_line, lines, TEMPLATES_FILES[i])

        with open(VERROU_FILES[i], "w") as file:
            file.writelines(lines)


if __name__ == "__main__":
    main()
