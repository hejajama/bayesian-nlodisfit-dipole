/*
 * Heikki Mäntysaari <heikki.mantysaari@jyu.fi>, 2020
 */

#include "tools.hpp"
#include <string>
#include <sstream>
#include <cmath>
#include <iostream>
#include <vector>
#include <gsl/gsl_integration.h>



/*
 * Str to double/int
 */
double StrToReal(std::string str)
{
    std::stringstream buff(str);
    double tmp;
    buff >> tmp;
    return tmp;
}

int StrToInt(std::string str)
{
    std::stringstream buff(str);
    int tmp;
    buff >> tmp;
    return tmp;
}

//

/* Returns index i for which
 * vec[i]<=val
 * Assumes that vec[i]<vec[i+1]
 * If such index can't be found, returns -1
 */

int FindIndex(double val, const std::vector<double>& vec)
{
    if (vec.empty())
    {
        std::cerr << "FindIndex: empty vector!" << std::endl;
        exit(1);
    }
    if (vec.empty() or val < vec.front())
        return -1;

    // Binary search for the largest i such that vec[i] <= val
    int left = 0;
    int right = static_cast<int>(vec.size()) - 1;
    int result = -1;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (vec[mid] <= val) {
            result = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    // If result is the last index or val < next element, return result
    if (result == -1)
        return -1;
    if (result == static_cast<int>(vec.size()) - 1 or vec[result + 1] > val)
        return result;

    return -1;
}

