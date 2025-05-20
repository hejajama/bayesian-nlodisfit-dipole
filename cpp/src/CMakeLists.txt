
add_library(
	amplitude
	STATIC
	amplitudelib.cpp
	datafile.cpp
	tools.cpp
	interpolation.cpp
)

add_executable(
	dipole
	dipole_amplitude.cpp
)

add_executable(
	test
    tests/tests.cpp
    tests/test_interpolation.cpp
)


target_link_libraries(
	dipole
	PRIVATE
	amplitude
	GSL::gsl
	GSL::gslcblas
)

target_link_libraries(
	test
	PRIVATE
	amplitude
	GSL::gsl
	GSL::gslcblas
)
