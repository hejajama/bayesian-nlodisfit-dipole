# Unit tests that test and demonstrate the functionality of the Python module
import unittest
import nlodipole 
import numpy as np

class TestNlodipole(unittest.TestCase):
    def test_GBW(self):
        # file data/gbw.dat corresponds to the GBW dipole amplitude
        # N(r,Y) = 1 - exp(-r^2 Q_s^2(Y)/4)
        # with Q_s^2(Y) = 1.0*exp(lambda*Y) [GeV^2] and lambda=1/3

        bk_file_dir = '../data/gbw.dat'  
        Y = 0.5
        gbwinterpolator = nlodipole.BKDipole(bk_file_dir)

        r_values = [1e-2, 1e-1, 1, 10]  # Example r values
        N_values = [gbwinterpolator.get_NrY(Y, r) for r in r_values]
        Qs2 = 1.0 * np.exp(1/3 * Y)  # Q_s^2(Y)
        true_values = [1. - np.exp(-r**2 * Qs2 / 4) for r in r_values]
        
        for computed, true in zip(N_values, true_values):
            self.assertAlmostEqual(computed, true, places=3)



        # Test evaluating the dipole at fixed Y and r
        r=0.2
        Y=2.6
        model=gbwinterpolator.get_NrY(Y=Y, r=r)
        Qs2 = 1.0 * np.exp(1/3 * Y) 
        true = 1.0 - np.exp(-r**2 * Qs2 / 4)
        self.assertAlmostEqual(model, true, places=3)

    def test_bal_sd_qs(self):
        bk_file_dir = "../data/balsd/bk_map.dat"
        Y=np.log(1/0.01)
        interpolator = nlodipole.BKDipole(bk_file_dir)

        # N(r^2=2/Q_s^2, Y) = 1 - exp(-0.5)
        # Check Q_s^2 quoted in Table 1
        true_qs2=0.196
        dipval = interpolator.get_NrY(Y, np.sqrt(2/true_qs2))
        self.assertAlmostEqual(dipval, 1 - np.exp(-0.5), places=2)

        bk_file_median = "../data/balsd/bk_median.dat"
        interpolator_median = nlodipole.BKDipole(bk_file_median)
        true_qs2_median = 0.203
        dipval=interpolator_median.get_NrY(Y, np.sqrt(2/true_qs2_median))
        self.assertAlmostEqual(dipval, 1 - np.exp(-0.5), places=2)

    def test_interpolation_boundaries(self):
        bk_file_dir = "../data/balsd/bk_map.dat"
        interpolator = nlodipole.BKDipole(bk_file_dir)

         # Check that we get NaN outside the range of the interpolator
        self.assertTrue(np.isnan( interpolator.get_NrY(1, 1e-20) )) # small r
        self.assertTrue(np.isnan( interpolator.get_NrY(1, 1e20) )) # large r
        self.assertTrue(np.isnan( interpolator.get_NrY(-1, 2) )) # negative Y = before initial condition
        self.assertTrue(np.isnan( interpolator.get_NrY(9999, 2) )) # too large Y

    def test_parent_qs(self):
        # Test the parent Q_s^2 for the Balitsky-Satya parent dipole
        bk_file_dir = "../data/pd/bk_map.dat"
        Y = np.log(1/0.01)
        interpolator = nlodipole.BKDipole(bk_file_dir)

        # Check Q_s^2 quoted in Table 1
        true_qs2 = 0.199
        dipval = interpolator.get_NrY(Y, np.sqrt(2/true_qs2))
        self.assertAlmostEqual(dipval, 1 - np.exp(-0.5), places=2)

        bk_file_dir = "../data/pd/bk_median.dat"
        interpolator_median = nlodipole.BKDipole(bk_file_dir)
        true_qs2_median = 0.208
        dipval = interpolator_median.get_NrY(Y, np.sqrt(2/true_qs2_median))
        self.assertAlmostEqual(dipval, 1 - np.exp(-0.5), places=2)

if __name__ == '__main__':
    unittest.main()