project(reSIProcateTest)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(PkgConfig)

file(GLOB SOURCE_FILES *.cxx)
include_directories(SYSTEM ${CONAN_INCLUDE_DIRS_RESIPROCATE})

add_executable(${CMAKE_PROJECT_NAME} ${SOURCE_FILES})
target_link_libraries(${CMAKE_PROJECT_NAME} ${CONAN_LIBS})
target_compile_options(${CMAKE_PROJECT_NAME} PUBLIC -Wno-deprecated-declarations)

enable_testing()
add_test(NAME test-all
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
         COMMAND ${CMAKE_PROJECT_NAME})
