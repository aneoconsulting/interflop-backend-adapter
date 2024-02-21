cmake_minimum_required(VERSION 3.12)


set(COMMON_PATH "${CMAKE_CURRENT_LIST_DIR}/verificarlo_env/common")
set(BACKENDS_PATH "${CMAKE_CURRENT_LIST_DIR}/verificarlo_env/backends")
file(GLOB BACKENDS_LIST "${BACKENDS_PATH}/*.cpp")

file(GLOB subdirectories LIST_DIRECTORIES true "${CMAKE_CURRENT_LIST_DIR}/verificarlo_env/backends/*")

foreach(subdirectory ${subdirectories})
    if(IS_DIRECTORY ${subdirectory})
        get_filename_component(BACKEND_NAME ${subdirectory} NAME)

        add_library("target_${BACKEND_NAME}" SHARED
            "${COMMON_PATH}/printf_specifier.c"
            "${COMMON_PATH}/logger.c"
            "${subdirectory}/complete_backend.c"
        )

        set_target_properties("target_${BACKEND_NAME}" PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_LIST_DIR}/backends_so")
    endif()
endforeach()
