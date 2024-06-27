

cmake_minimum_required (VERSION 3.20)

project(Test_Result)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

add_executable(test_verificarlo_res Test_Frontend_executable.cpp)
add_executable(test_verrou_res Test_Frontend_executable.cpp)

set_property(TARGET test_verrou_res PROPERTY CXX_STANDARD 17)

set(PYTHON_SCRIPT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/test_result.py)
get_filename_component(PARENT_DIR ${CMAKE_SOURCE_DIR} DIRECTORY)
get_filename_component(GRANDPARENT_DIR ${PARENT_DIR} DIRECTORY)
set(PIN_PATH ${PARENT_DIR}/pene_files/PENE/Pin/Linux/pin)
set(LIB_PATH ${PARENT_DIR}/pene_files/PENE/src/libpene.so)

# set(CMAKE_GENERICS_PATH "${CMAKE_SOURCE_DIR}")


set(new_back_verificarlo ${PARENT_DIR}/verificarlo_files/backends_so/libtarget_backend_test_2.so)

set(TOOL_PATH ${PARENT_DIR}/pene_files/PENE/cmake/tools)

add_custom_command(
    TARGET test_verificarlo_res
    PRE_BUILD
    COMMAND verificarlo-c++ ${CMAKE_CURRENT_SOURCE_DIR}/Test_Frontend_executable.cpp -o ${CMAKE_CURRENT_BINARY_DIR}/verificarlo_exe 
    COMMENT "Building verificarlo_exe"
)

add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/test_result.py
  COMMAND ${CMAKE_COMMAND} 
          -D INFILE=${CMAKE_CURRENT_SOURCE_DIR}/test_result.py
          -D OUTFILE=${CMAKE_CURRENT_BINARY_DIR}/test_result.py
          -D REPLACE_TESTS_BINARY_DIR=${CMAKE_CURRENT_BINARY_DIR}
          -D VERIFICARLO_EXECUTABLE=${CMAKE_CURRENT_BINARY_DIR}/verificarlo_exe 
          -D BACKEND_VERIFICARLO=${new_back_verificarlo}
		      -D VERROU_EXECUTABLE=$<TARGET_FILE:test_verrou_res>
          -D LIB=${LIB_PATH}
          -D PIN_EXECUTABLE=${PIN_PATH}
          -P ${CMAKE_GENERICS_PATH}/GenericConfigureFile.cmake
  DEPENDS
    ${CMAKE_GENERICS_PATH}/GenericConfigureFile.cmake
  COMMENT "Configuring test_result.py"
  VERBATIM
)


set(TEST_SCRIPTS test_result.py)


list(TRANSFORM TEST_SCRIPTS PREPEND ${CMAKE_CURRENT_BINARY_DIR}/)
add_custom_target(${PROJECT_NAME} ALL DEPENDS 
    ${TEST_SCRIPTS}
    ${CMAKE_CURRENT_BINARY_DIR}/test_result.py
)

enable_testing()


# Run each test function individually
set(TEST_LIST test_result_PENE test_result_Verificarlo)

find_package(Python3 REQUIRED Interpreter)
foreach(test ${TEST_LIST})
    add_test(NAME ${test}
      COMMAND ${Python3_EXECUTABLE} -m pytest -k ${test} ${CMAKE_CURRENT_BINARY_DIR}/test_result.py)
endforeach()

include_directories("../../pene_files/PENE/Pin/Linux")
include_directories("../../pene_files/PENE/src")
