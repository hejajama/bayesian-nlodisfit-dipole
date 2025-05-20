# NLO DIS fit

This repository contains Python and C++ codes to evaluate dipole amplitudes using grids from the NLO DIS fit published in C. Casuga et al.

## Python

## C++
The C++ code can be found from the cpp folder. It requires GSL, and CMake is used to compile the code.

### Compile
To compile, in the `cpp` folder run
```bash
mkdir build
cd build
cmake ..
make
```

### Test 
In order to check that the setup works without problems, run unit tests by running in the `cpp` folder the command
```bash
./build/bin/test
```
All tests should pass. The tests cover internal code dynamcis and also reproduce some numbers reported in the publication.

There is also an example code `cpp/src/dipole_amplitude.cpp` that is compiled to produce the binary `build/bin/dipole`. That code takes as an input the BK datafile:
```bash
./build/bin/dipole path/to/bk/datafile
```

### Usage
See `cpp/src/amplitudelib.hpp` for details. For examples, see `cpp/src/dipole_amplitude.cpp` and `cpp/src/tests/tests.cpp`

Typical workflow as an example:
```c++
const std::string datafile="../data/median_balsd_bk.dat";
// Read data
AmplitudeLib dipole(datafile);

// Evaluate dipole at r=0.4 GeV^-1 at evolution rapidity Y=0.3
double Y=0.3;
cout << "N(r=0.4 GeV^-1, Y=0.3) = " << dipole.DipoleAmplitude(0.4, Y) << endl;

// If you are evaluating the dipole many times at the same evolution rapidity, 
// to speed up the evaluation one can initialize the interpolation first
dipole.InitializeInterpolation(Y);
```