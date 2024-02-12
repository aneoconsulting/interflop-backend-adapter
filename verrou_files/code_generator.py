#!/bin/python3.11

from os import makedirs
from patch import fromfile
from jinja2 import Template

from code_generator_const import *


def patch_file(diff_path):
    patch = fromfile(diff_path)
    patch.apply()


def remove_prev_gen_code(lines, head_line, index):
    while lines[head_line] != GENERATED_FOOTERS[index]:
        del lines[head_line]

    return lines


def get_op_codes():
    op_codes = []

    with open(BACKEND_PATH, "r") as file:
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


def add_template_lines(header_line, lines, template_path):
    with open(template_path, "r") as file:
        template = Template(file.read())
    correct_text = template.render(backend_nb=BACKEND_NB, backend_names=[BACKEND_NAME], backend_call_names=[BACKEND_CALL_NAME])
    correct_lines = correct_text.splitlines(keepends=True)

    lines_applied = lines[:header_line] + correct_lines + lines[header_line:]

    return lines_applied


def prepare_verrou_files_for_new_backends():
    for i in range(len(VERROU_FILES)):
        with open(VERROU_FILES[i], "r") as file:
            try:
                lines = file.readlines()
                header_line = lines.index(GENERATED_HEADERS[i]) + 1
            except (ValueError):
                lines = []
                header_line = -1

        if header_line < 0:
            patch_file(DIFF_FILES[i])
            with open(VERROU_FILES[i], "r") as refreshed_file:
                lines = refreshed_file.readlines()
            header_line = lines.index(GENERATED_HEADERS[i]) + 1
        else:
            lines = remove_prev_gen_code(lines, header_line, i)

        lines = add_template_lines(header_line, lines, TEMPLATES_FILES[i])

        with open(VERROU_FILES[i], "w") as file:
            file.writelines(lines)


def create_backend_files():
    op_codes = get_op_codes()

    with open(TEMPLATE_BACK_C, "r") as file:
        c_template = Template(file.read())
    correct_c = c_template.render(
        backend_name=BACKEND_NAME,
        backend_call_name=BACKEND_CALL_NAME,
        upper_backend_call_name=BACKEND_CALL_NAME.upper(),
        add_float_code=op_codes[0],
        sub_float_code=op_codes[1],
        mul_float_code=op_codes[2],
        div_float_code=op_codes[3],
        cmp_float_code=op_codes[4],
        madd_float_code="",
        sqrt_float_code="",

        add_double_code=op_codes[5],
        sub_double_code=op_codes[6],
        mul_double_code=op_codes[7],
        div_double_code=op_codes[8],
        cmp_double_code=op_codes[9],
        madd_double_code="",
        sqrt_double_code=""
    )
    with open(COMPLETE_BACK_C, "w") as file:
        file.write(correct_c)

    with open(TEMPLATE_BACK_H, "r") as file:
        h_template = Template(file.read())
    correct_h = h_template.render(
        backend_name=BACKEND_NAME,
        backend_call_name=BACKEND_CALL_NAME,
        upper_backend_call_name=BACKEND_CALL_NAME.upper()
    )

    with open(COMPLETE_BACK_H, "w") as file:
        file.write(correct_h)


def add_new_backends():
    create_backend_files()


def main():
    prepare_verrou_files_for_new_backends()
    add_new_backends()


if __name__ == "__main__":
    main()
