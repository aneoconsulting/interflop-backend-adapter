cmake_minimum_required(VERSION 3.12)

message(STATUS "Creating backends for PENE tool.${CMAKE_CURRENT_LIST_DIR}")

execute_process(COMMAND python3 ./code_generator.py WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})

set(COMPLETED_REPLACE_MODULE    "${CMAKE_CURRENT_LIST_DIR}/completed_pene_files/replace_module.cpp")
set(SOURCE_REPLACE_MODULE       "${CMAKE_CURRENT_LIST_DIR}/PENE/src/replace_module.cpp")

file(RENAME "${COMPLETED_REPLACE_MODULE}"            "${SOURCE_REPLACE_MODULE}")

set(COMPLETED_FILES_PATH "${CMAKE_CURRENT_LIST_DIR}/completed_pene_files")
set(PENE_BACKENDS_PATH "${CMAKE_CURRENT_LIST_DIR}/PENE/include/replace/backend")
file(GLOB subdirectories LIST_DIRECTORIES true ${CMAKE_CURRENT_SOURCE_DIR}/backend/*)

foreach(subdirectory ${subdirectories})
    if(IS_DIRECTORY ${subdirectory})
        get_filename_component(FOLDER_NAME ${subdirectory} NAME)

        message(STATUS "Building ${FOLDER_NAME} backend into the PENE repository.")

        set(BACKEND_FOLD_PATH "${PENE_BACKENDS_PATH}/backend_${FOLDER_NAME}")

        file(MAKE_DIRECTORY "${BACKEND_FOLD_PATH}")
        file(RENAME "${COMPLETED_FILES_PATH}/complete_backend_${FOLDER_NAME}.h"
                    "${BACKEND_FOLD_PATH}/interflop_${FOLDER_NAME}.h")
    endif()
endforeach()

message(STATUS "Building and compiling PENE.")

execute_process(COMMAND "cmake" "." WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/PENE")
execute_process(COMMAND "cmake" "--build" "." WORKING_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/PENE")