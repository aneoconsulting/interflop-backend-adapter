cmake_minimum_required(VERSION 3.12)

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