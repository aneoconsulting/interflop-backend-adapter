
cmake_minimum_required(VERSION 3.12)

project(Tests_All_Frontend)


set(CMAKE_GENERICS_PATH "${CMAKE_SOURCE_DIR}")

set(CMAKE_SKIP_BUILD_RPATH FALSE)

set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

enable_testing()

add_subdirectory("Test_result") 
add_subdirectory("Test_counter")
add_subdirectory("Test_binary") 