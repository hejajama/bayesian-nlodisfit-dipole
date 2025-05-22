import sys
import matplotlib.pyplot as plt
from funcs import *

def main(bk_file_dir, x):
    """
    Prints and plots the values of N(Y, r) for the given rapidity Y = ln(1/x).

    Args:
        bk_file_dir (str): Path to the file containing the BK data.
        x (float): Value of Bjorken-x, where Y = ln(1/x).
    """
    Y = np.log(1.0/x)
    r_values, N_values = get_Nr(bk_file_dir, Y)
    print(f"### for Y = {Y}")
    print("### r (GeV^-1), N")
    for r, N in zip(r_values, N_values):
        print(f"{r:.6e} {N:.6e}")

    # Plot the results
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(r_values, N_values, linestyle='-', color='b',  label=f'Y=ln(1/{x})')
    ax.set_xscale('log')
    #ax.set_yscale('log')
    ax.set_xlabel(r'$r$ (GeV$^{-1}$)')
    ax.set_ylabel(r'$N(Y, r)$')
    ax.set_xlim(0.5e-1, 1e2)
    ax.legend()
    fig.savefig(f'Nr_Y_{Y:.2f}.pdf')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python read_bk.py <bk_file_dir> <Y>")
        sys.exit(1)
    bk_file_dir = sys.argv[1]
    x = float(sys.argv[2])

    main(bk_file_dir, x)

