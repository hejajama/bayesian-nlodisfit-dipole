#include "unit_test_framework.hpp"
#include <cmath>
#include <string>

#include "../amplitudelib.hpp"

const std::string gbw_datafile = "../data/gbw.dat";


TEST(GBW_DIPOLE_SATSCALE)
{
    // file gbw.dat corresponds to the GBW dipole amplitude
    // N(r,Y) = 1 - exp(-r^2 Q_s^2(Y)/4)
    // with Q_s^2(Y) = 1.0*exp(-lambda*Y) [GeV^2] and lambda=1/3
    AmplitudeLib N(gbw_datafile);

    double Ns=1-std::exp(-0.5);

    // Test initial condition
    ASSERT_ALMOST_EQUAL(N.SaturationScale(0, Ns), 1.0, 1e-3);

    // Test evolution rapidity that is not part of the grid
    double Y=std::log(0.01/0.001);
    // Test first without iniitalizing interpolation at fixed Y
    ASSERT_ALMOST_EQUAL(N.SaturationScale(Y, Ns), std::exp(1./3.*Y), 1e-3);
    // Then faster versoin with pre-initialized interpolation
    N.InitializeInterpolation(Y);
    ASSERT_ALMOST_EQUAL(N.SaturationScale(Y, Ns), std::exp(1./3.*Y), 1e-3);

}


TEST(GBW_DIPOLE_OUT_OF_RANGE)
{
    // file gbw.dat correspondds to the GBW dipole amplitude
    // N(r,Y) = 1 - exp(-r^2 Q_s^2(Y)/4)
    // with Q_s^2(Y) = 1.0*exp(-lambda*Y) [GeV^2] and lambda=1/3
    AmplitudeLib N(gbw_datafile);
    N.SetOutOfRangeErrors(false);

    // Very small or very large dipole 
    ASSERT_ALMOST_EQUAL(N.DipoleAmplitude(1e-30, 0.1), 0, 1e-5);
    ASSERT_ALMOST_EQUAL(N.DipoleAmplitude(1e10, 2.4), 1, 1e-5);
}

TEST(INTERPOLATE_GBW_DIPOLE)
{
    double Y = 2.05;
    double qs2 = 1.0*std::exp(1./3.*2.05);
    double r = 0.2;
    double gbw = 1-std::exp(-qs2*r*r/4);
    AmplitudeLib N(gbw_datafile);
    ASSERT_ALMOST_EQUAL(gbw, N.DipoleAmplitude(r,Y), 1e-4);
}

TEST(BAL_SD_MEDIAN_MAP_QS)
{
    // Check that we reproduce the saturation scale reported in Table 1 of the paper
    AmplitudeLib N("../data/balsd/bk_median.dat");
    double Ns = 1-std::exp(-0.5);
    double Y = std::log(1/0.01);
    double qs2 = N.SaturationScale(Y, Ns);
    ASSERT_ALMOST_EQUAL(qs2, 0.203, 1e-3);
    
    AmplitudeLib N2("../data/balsd/bk_map.dat");
    qs2 = N2.SaturationScale(Y, Ns);
    ASSERT_ALMOST_EQUAL(qs2, 0.196, 1e-3);
}

TEST(PARENT_DIPOLE_MEDIAN_MAP_QS)
{
    // Check that we reproduce the saturation scale reported in Table 1 of the paper
    AmplitudeLib N("../data/pd/bk_median.dat");
    double Ns = 1-std::exp(-0.5);
    double Y = std::log(1/0.01);
    double qs2 = N.SaturationScale(Y, Ns);
    ASSERT_ALMOST_EQUAL(qs2, 0.208, 1e-3);
    
    AmplitudeLib N2("../data/pd/bk_map.dat");
    qs2 = N2.SaturationScale(Y, Ns);
    ASSERT_ALMOST_EQUAL(qs2, 0.199, 1e-3);
}


TEST_MAIN()
