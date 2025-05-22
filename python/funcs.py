import numpy as np
import scipy.interpolate as interpolate

def ReadBKDipole(thefile): # 
    '''
    Reads the dipole amplitude from the given datafile produced running BK solver from 
    
    Returns an interpolator for the dipole: N(Y, r), where r is in GeV^-1, and x = x_0*exp(Y)
    '''

    with open(thefile) as f:
        content = f.read().split("###")
    
    content = content[1:]   # gets rid of the stuff at the beginning
    content = [i.split() for i in content] # cleans up lines
    NrY_data = []
    pars = []
    for i in content:

        x = list(map(float, i))
        if len(x) == 1:
            pars.append(x)
        else:
            NrY_data.append(x)

        
    rmYs = np.array(NrY_data).T[1:]     # removes Y values
    N_values = rmYs.T
    Y_values = np.array(NrY_data).T[0]

    pars = np.ndarray.flatten(np.array(pars))
    minr = pars[0]
    mult = pars[1]
    n = int(pars[2])
    r_values = np.array([minr*mult**i for i in range(n)])
    
    
    rgrid=[]
    ygrid=[]
    for y in Y_values:
        for r in r_values:
            rgrid.append(r)
            ygrid.append(y)
    
    interpolator = interpolate.CloughTocher2DInterpolator((ygrid, rgrid), N_values.flatten(), fill_value=1.0)
    
    return interpolator

def get_NRY(bk_file_dir, Y, r):
    '''
    Returns the value of N(Y,r) for the given Y and r
    '''
    bk_interpolator = ReadBKDipole(bk_file_dir)
    return bk_interpolator(Y, r)

def get_Nr(bk_file_dir, Y, r_min = 1e-3, r_max = 1e2, r_points = 50):
    '''
    Returns N for the given Y over points in r logspace
    '''
    bk_interpolator = ReadBKDipole(bk_file_dir)
    r_values = np.logspace(np.log10(r_min), np.log10(r_max), r_points)
    N_values = np.array([bk_interpolator(Y, r) for r in r_values])
    return r_values, N_values

# load all bk files and make list of interpolators
def get_dipole_interpolators(bk_folder):
    '''       
    Returns list of interpolators for each BK file given bk_folder.
    '''
    import os
    bk_interpolators = []
    bk_folder_list = os.listdir(bk_folder)
    for i in range(len(bk_folder_list)):
        print(f"Reading file: {i+1}/{len(bk_folder_list)}")
        bk_file = os.path.join(bk_folder, os.listdir(bk_folder)[i])
        bk_interpolators.append(ReadBKDipole(bk_file))

    return bk_interpolators

def get_sd(values, mean):
    
    ''' Returns standard deviation of values above or below mean '''

    up_sd = np.std(values[values > mean])
    down_sd = np.std(values[values < mean])
    print('how many values greater than mean', len(values[values > mean]))
    print('how many values less than mean', len(values[values < mean]))
    # print('up_sd', up_sd)
    # print('down_sd', down_sd)
    # print('mean', mean)

    return up_sd, down_sd

def get_dipole_mean_upsd_downsd(bk_interpolators, rs, Y = np.log(1/0.01)):
    '''
    Returns the mean and upper/lower standard deviation of func for a given an array of r and rapidity Y.
    '''
    mean = []
    up_sd = []
    down_sd = []

    if len(rs.shape) != 1:
        raise ValueError("r must be a 1D array")
    
    for r in rs:
        val_per_r = np.array([bk_interpolators[i](Y, r) for i in range(len(bk_interpolators))])
        val_per_r_mean = np.mean(val_per_r)
        mean.append(val_per_r_mean)
        up_sd_r, down_sd_r = get_sd(val_per_r, val_per_r_mean)
        up_sd.append(up_sd_r)
        down_sd.append(down_sd_r)
    
    return np.array(mean), np.array(up_sd), np.array(down_sd)