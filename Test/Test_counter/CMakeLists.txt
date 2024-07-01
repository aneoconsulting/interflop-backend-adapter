


cmake_minimum_required (VERSION 3.20)

project(Test_Counter)

find_package(Python3 COMPONENTS Interpreter REQUIRED)

add_executable(test_verificarlo Test_Frontend_executable.cpp)
add_executable(test_verrou Test_Frontend_executable.cpp)

set_property(TARGET test_verrou PROPERTY CXX_STANDARD 17)

set(PYTHON_SCRIPT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/test_counter.py)
get_filename_component(PARENT_DIR ${CMAKE_SOURCE_DIR} DIRECTORY)
get_filename_component(GRANDPARENT_DIR ${PARENT_DIR} DIRECTORY)
get_filename_component(GRAND_GRAND_DIR ${GRANDPARENT_DIR} DIRECTORY)
set(PIN_PATH ${PARENT_DIR}/pene_files/PENE/Pin/Linux/pin)
set(LIB_PATH ${PARENT_DIR}/pene_files/PENE/src/libpene.so)

# set(CMAKE_GENERICS_PATH "${CMAKE_SOURCE_DIR}")

set(new_back_verificarlo ${PARENT_DIR}/verificarlo_files/backends_so/libtarget_backend_test_2.so)

set(TOOL_PATH ${PARENT_DIR}/pene_files/PENE/cmake/tools)

add_custom_command(
    TARGET test_verificarlo
    PRE_BUILD
    COMMAND verificarlo-c++ ${CMAKE_CURRENT_SOURCE_DIR}/Test_Frontend_executable.cpp -o ${CMAKE_CURRENT_BINARY_DIR}/verificarlo_exe 
    COMMENT "Building verificarlo_exe"
)

add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/test_counter.py
  COMMAND ${CMAKE_COMMAND} 
          -D INFILE=${CMAKE_CURRENT_SOURCE_DIR}/test_counter.py
          -D OUTFILE=${CMAKE_CURRENT_BINARY_DIR}/test_counter.py
          -D REPLACE_TESTS_BINARY_DIR=${CMAKE_CURRENT_BINARY_DIR}
          -D VERIFICARLO_EXECUTABLE=${CMAKE_CURRENT_BINARY_DIR}/verificarlo_exe 
          -D BACKEND_VERIFICARLO=${new_back_verificarlo}
		      -D VERROU_EXECUTABLE=$<TARGET_FILE:test_verrou>
          -D LIB=${LIB_PATH}
          -D PIN_EXECUTABLE=${PIN_PATH}
          -P ${CMAKE_GENERICS_PATH}/GenericConfigureFile.cmake
  DEPENDS
    ${CMAKE_GENERICS_PATH}/GenericConfigureFile.cmake
  COMMENT "Configuring test_replace.py"
  VERBATIM
)


set(TEST_SCRIPTS test_counter.py)

list(TRANSFORM TEST_SCRIPTS PREPEND ${CMAKE_CURRENT_BINARY_DIR}/)
add_custom_target(${PROJECT_NAME} ALL DEPENDS 
    ${TEST_SCRIPTS}
    ${CMAKE_CURRENT_BINARY_DIR}/test_counter.py
)

enable_testing()


option(TEST_PENE "Enable testing for PENE" OFF)
option(TEST_VERIFICARLO "Enable testing for Verificarlo" OFF)

set(PENE_TESTS test_Nbr_Op_PENE)
set(VERIFICARLO_TESTS test_Nbr_Op_Verificarlo)

set(TEST_LIST)

if(TEST_PENE)
    list(APPEND TEST_LIST ${PENE_TESTS})
endif()

if(TEST_VERIFICARLO)
    list(APPEND TEST_LIST ${VERIFICARLO_TESTS})
endif()


if(NOT "${TEST_LIST}" STREQUAL "")
    foreach(test ${TEST_LIST})
        add_test(NAME ${test}
            COMMAND ${Python3_EXECUTABLE} -m pytest -k ${test} ${CMAKE_CURRENT_BINARY_DIR}/test_counter.py
        )
    endforeach()
else()
    message(WARNING "No tests specified. Please enable either TEST_PENE or TEST_VERIFICARLO to run specific tests.")
endif()


include_directories("../../../pene_files/PENE/Pin/Linux")
include_directories("../../../pene_files/PENE/src")
