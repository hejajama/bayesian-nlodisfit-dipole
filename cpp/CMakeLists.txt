# stop if cmake version is below 3.0
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)

project(nlodisfit CXX C)

set(CMAKE_BUILD_TYPE Release)

find_package(GSL REQUIRED)
include_directories(${GSL_INCLUDE_DIRS})

add_subdirectory(src)

set_target_properties(amplitude PROPERTIES
	 LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib
	ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib )

set_target_properties(dipole PROPERTIES
	RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set_target_properties(test PROPERTIES
	RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
