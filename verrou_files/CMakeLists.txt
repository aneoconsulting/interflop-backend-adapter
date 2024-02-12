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
        file(COPY_FILE "${subdirectory}/complete_backend.cpp"
            "${BACKEND_FOLD_PATH}/interflop_custom.cxx")
        file(COPY_FILE "${subdirectory}/complete_backend.h"
            "${BACKEND_FOLD_PATH}/interflop_custom.h")
    endif()
endforeach()

message(STATUS "Building and compiling verrou.")
execute_process(COMMAND "${VALGRIND_PATH}/autogen.sh" WORKING_DIRECTORY ${VALGRIND_PATH})
execute_process(COMMAND "${VALGRIND_PATH}/configure --enable-only64bit --prefix=${CMAKE_CURRENT_LIST_DIR}/verrou_repo/verrou_software"
                WORKING_DIRECTORY ${VALGRIND_PATH})
execute_process(COMMAND "make" WORKING_DIRECTORY ${VALGRIND_PATH})
execute_process(COMMAND "make install" WORKING_DIRECTORY ${VALGRIND_PATH})