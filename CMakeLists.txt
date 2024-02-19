cmake_minimum_required(VERSION 3.12)

project(Interflop-backend-adapter)

option(BUILD_FOR_PENE "Build backend shared object for the PENE tool" OFF)
option(BUILD_FOR_VERIFICARLO "Build backend shared object for the Verificarlo tool" OFF)
option(BUILD_FOR_VERROU "Build backend in the Verrou repository" OFF)


if(BUILD_FOR_PENE)
    include("${CMAKE_CURRENT_SOURCE_DIR}/pene_files/CMakeLists.txt")
endif()


if(BUILD_FOR_VERIFICARLO)
    include("${CMAKE_CURRENT_SOURCE_DIR}/verificarlo_files/CMakeLists.txt")
endif()


if(BUILD_FOR_VERROU)
    include("${CMAKE_CURRENT_SOURCE_DIR}/verrou_files/CMakeLists.txt")
endif()