cmake_minimum_required(VERSION 3.12)

project(YourProjectName)

set(PENE_PATH "NONE" CACHE STRING "Build backend in the PENE repository")
set(VERIFICARLO_PATH "NONE" CACHE STRING "Build backend in the Verificarlo repository")
set(VERROU_PATH "NONE" CACHE STRING "Build backend in the Verrou repository")


if(NOT "${PENE_PATH}" STREQUAL "NONE")
    set(PENE_SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/pene_files/backend.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/pene_files/interflop_header.hpp
    )

    file(TO_CMAKE_PATH "${PENE_PATH}/test/custom_pene_backend.so" PENE_BACKEND_PATH)

    message(STATUS "Building backend to PENE path: \"${PENE_BACKEND_PATH}\"")

    configure_file("${CMAKE_CURRENT_SOURCE_DIR}/backend/backend.cpp" "${CMAKE_CURRENT_SOURCE_DIR}/pene_files/backend.cpp" COPYONLY)

    add_library(pene_custom_backend SHARED ${PENE_SOURCE_FILES})

    set_target_properties(pene_custom_backend PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/output
    )

    add_custom_command(TARGET pene_custom_backend POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:pene_custom_backend> "${PENE_BACKEND_PATH}${TARGET_FILE}"
    )

    add_custom_command(TARGET pene_custom_backend POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E remove "${CMAKE_CURRENT_SOURCE_DIR}/pene_files/backend.cpp"
    )
endif()


if(NOT "${VERIFICARLO_PATH}" STREQUAL "NONE")
    set(VERIF_SOURCE_FILES
        ${CMAKE_CURRENT_SOURCE_DIR}/verificarlo_files/backend.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/verificarlo_files/interflop_header.hpp
    )

    file(TO_CMAKE_PATH "${VERIFICARLO_PATH}/test/custom_verificarlo_backend.so" VERIFICARLO_BACKEND_PATH)

    message(STATUS "Building backend to Verificarlo path: \"${VERIFICARLO_BACKEND_PATH}\"")

    configure_file("${CMAKE_CURRENT_SOURCE_DIR}/backend/backend.cpp" "${CMAKE_CURRENT_SOURCE_DIR}/verificarlo_files/backend.cpp" COPYONLY)

    add_library(verif_custom_backend SHARED ${VERIF_SOURCE_FILES})

    set_target_properties(verif_custom_backend PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/output
    )

    add_custom_command(TARGET verif_custom_backend POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:verif_custom_backend> "${VERIFICARLO_BACKEND_PATH}${TARGET_FILE}"
    )

    add_custom_command(TARGET verif_custom_backend POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E remove "${CMAKE_CURRENT_SOURCE_DIR}/verificarlo_files/backend.cpp"
    )
endif()


if(NOT "${VERROU_PATH}" STREQUAL "NONE")
    file(TO_CMAKE_PATH "${VERROU_PATH}/test/custom_verrou_backend.so" VERROU_BACKEND_PATH)

    message(STATUS "(Not implemented) Building backend to Verrou path: \"${VERROU_BACKEND_PATH}\"")
endif()