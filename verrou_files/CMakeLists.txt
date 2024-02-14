cmake_minimum_required(VERSION 3.12)


set(VALGRIND_PATH "${CMAKE_CURRENT_LIST_DIR}/verrou_repo/valgrind-3.22.0+verrou-dev")
set(VERROU_BACKENDS_PATH "${VALGRIND_PATH}/verrou/interflop_backends")

set(COMPLETED_FILES_PATH "${CMAKE_CURRENT_LIST_DIR}/completed_verrou_files")

set(COMPLETED_VR_MAIN_C             "${COMPLETED_FILES_PATH}/vr_main.c")
set(COMPLETED_VR_MAIN_H             "${COMPLETED_FILES_PATH}/vr_main.h")
set(COMPLETED_VR_CLO_C              "${COMPLETED_FILES_PATH}/vr_clo.c")
set(COMPLETED_MAKEFILE_AM           "${COMPLETED_FILES_PATH}/makefile.am")
set(COMPLETED_STATIC_INTEG_BACK_H   "${COMPLETED_FILES_PATH}/statically_integrated_backends.h")
set(COMPLETED_GEN_BACK_INTER_OP_PY  "${COMPLETED_FILES_PATH}/generateBackendInterOperator.py")

set(SOURCE_VR_MAIN_C                "${VALGRIND_PATH}/verrou/vr_main.c")
set(SOURCE_VR_MAIN_H                "${VALGRIND_PATH}/verrou/vr_main.h")
set(SOURCE_VR_CLO_C                 "${VALGRIND_PATH}/verrou/vr_clo.c")
set(SOURCE_MAKEFILE_AM              "${VALGRIND_PATH}/verrou/Makefile.am")
set(SOURCE_STATIC_INTEG_BACK_H      "${VALGRIND_PATH}/verrou/interflop_backends/statically_integrated_backends.h")
set(SOURCE_GEN_BACK_INTER_OP_PY     "${VALGRIND_PATH}/verrou/generateBackendInterOperator.py")

message(STATUS "Creating backends for Verrou tool.${CMAKE_CURRENT_LIST_DIR}")

execute_process(COMMAND python3 ./code_generator.py WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

file(RENAME "${COMPLETED_VR_MAIN_C}"            "${SOURCE_VR_MAIN_C}")
file(RENAME "${COMPLETED_VR_MAIN_H}"            "${SOURCE_VR_MAIN_H}")
file(RENAME "${COMPLETED_VR_CLO_C}"             "${SOURCE_VR_CLO_C}")
file(RENAME "${COMPLETED_MAKEFILE_AM}"          "${SOURCE_MAKEFILE_AM}")
file(RENAME "${COMPLETED_STATIC_INTEG_BACK_H}"  "${SOURCE_STATIC_INTEG_BACK_H}")
file(RENAME "${COMPLETED_GEN_BACK_INTER_OP_PY}" "${SOURCE_GEN_BACK_INTER_OP_PY}")

file(GLOB subdirectories LIST_DIRECTORIES true ${CMAKE_CURRENT_SOURCE_DIR}/backend/*)

foreach(subdirectory ${subdirectories})
    if(IS_DIRECTORY ${subdirectory})
        get_filename_component(FOLDER_NAME ${subdirectory} NAME)

        message(STATUS "Building ${FOLDER_NAME} backend into the verrou repository.")

        set(BACKEND_FOLD_PATH "${VERROU_BACKENDS_PATH}/backend_${FOLDER_NAME}")

        file(MAKE_DIRECTORY "${BACKEND_FOLD_PATH}")
        file(RENAME "${subdirectory}/complete_backend.cpp"
                    "${BACKEND_FOLD_PATH}/interflop_${FOLDER_NAME}.cxx")
        file(RENAME "${subdirectory}/complete_backend.h"
                    "${BACKEND_FOLD_PATH}/interflop_${FOLDER_NAME}.h")
    endif()
endforeach()

execute_process(COMMAND python3 generateBackendInterOperator.py WORKING_DIRECTORY "${VALGRIND_PATH}/verrou/")

message(STATUS "Building and compiling verrou. ${VALGRIND_PATH}")
execute_process(COMMAND "./autogen.sh" WORKING_DIRECTORY ${VALGRIND_PATH})
execute_process(COMMAND "./configure" "--enable-only64bit" "--prefix=${CMAKE_CURRENT_LIST_DIR}/verrou_repo/verrou_software"
                WORKING_DIRECTORY "${VALGRIND_PATH}")
execute_process(COMMAND "make" WORKING_DIRECTORY ${VALGRIND_PATH})
execute_process(COMMAND "make" "install" WORKING_DIRECTORY ${VALGRIND_PATH})