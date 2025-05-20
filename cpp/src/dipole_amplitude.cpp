/*
 * Example code: how to read BK solution and extract dipole amplitude
 *
 * Heikki Mäntysaari <heikki.mantysaari@jyu.fi>, 2019
 */

#include "amplitudelib.hpp"
#include <string>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <ctime>
#include <unistd.h>

using namespace std;



int main(int argc, char* argv[])
{   
    string datafile=argv[1];

    // Read data
    AmplitudeLib N(datafile);
    //cout  << N.GetString() << endl;
    
    const double Ns =  1.0-std::exp(-0.5);
    
    // Note: If I were to evaluate N many times at the same evolution
    // rapidity, I should do 
    double Y = std::log(1./0.01);  
    N.InitializeInterpolation(Y);
    cout << N.SaturationScale(std::log(1./0.01), Ns) << endl; exit(1);

    cout << "# Q_s^2(Y=ln(1/0.01)) = " << N.SaturationScale(std::log(1./1), Ns) << " GeV^2" << endl;
    
    
    cout << "# r [1/GeV]   N(r,Y=ln(1/0.01))" << endl;
    double minr = N.MinR()*1.01; double maxr=N.MaxR()*0.99;
    for (double r=minr; r<maxr; r*=3)
    {
        cout << std::scientific << std::setprecision(9) << r << " "  << N.DipoleAmplitude(r, Y)  << endl;
    }

     
    return 0;
}
