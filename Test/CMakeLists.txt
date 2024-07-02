
cmake_minimum_required(VERSION 3.12)

project(Tests_All_Frontend)


set(CMAKE_GENERICS_PATH "${CMAKE_SOURCE_DIR}")

enable_testing()

add_subdirectory("Test_result")  
add_subdirectory("Test_counter")  
add_subdirectory("Test_binary")   
