cmake_minimum_required(VERSION 3.12)


message(STATUS "Building backends for Verrou tool.")

set(VALGRIND_PATH "${CMAKE_CURRENT_LIST_DIR}/verrou_repo/valgrind-3.22.0+verrou-dev")

execute_process(COMMAND python3 code_generator.py WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

file(GLOB subdirectories LIST_DIRECTORIES true ${CMAKE_CURRENT_SOURCE_DIR}/backend/*)

foreach(subdirectory ${subdirectories})
    if(IS_DIRECTORY ${subdirectory})
        get_filename_component(FOLDER_NAME ${subdirectory} NAME)

        message(STATUS "Building ${FOLDER_NAME} backend into the verrou repository.")

        set(BACKEND_FOLD_PATH "${CMAKE_CURRENT_LIST_DIR}/verrou_repo/valgrind-3.22.0+verrou-dev/verrou/interflop_backends/backend_${FOLDER_NAME}")

        file(MAKE_DIRECTORY "${BACKEND_FOLD_PATH}")
        file(RENAME "${subdirectory}/complete_backend.cpp"
            "${BACKEND_FOLD_PATH}/interflop_${FOLDER_NAME}.cxx")
        file(RENAME "${subdirectory}/complete_backend.h"
            "${BACKEND_FOLD_PATH}/interflop_${FOLDER_NAME}.h")
    endif()
endforeach()

execute_process(COMMAND python3 generateBackendInterOperator.py WORKING_DIRECTORY "${VALGRIND_PATH}/verrou/")

message(STATUS "Building and compiling verrou. ${VALGRIND_PATH}")
execute_process(COMMAND "./autogen.sh" WORKING_DIRECTORY ${VALGRIND_PATH} RESULT_VARIABLE ret)
execute_process(COMMAND "./configure" "--enable-only64bit" "--prefix=${CMAKE_CURRENT_LIST_DIR}/verrou_repo/verrou_software"
                WORKING_DIRECTORY "${VALGRIND_PATH}" RESULT_VARIABLE ret)
execute_process(COMMAND "make" WORKING_DIRECTORY ${VALGRIND_PATH} RESULT_VARIABLE ret)
execute_process(COMMAND "make" "install" WORKING_DIRECTORY ${VALGRIND_PATH} RESULT_VARIABLE ret)