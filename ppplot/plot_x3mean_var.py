# Coordinate system: Cartesian
# Data dimensions: time x1 x2 x3
# Description: plot x3-mean variable (similar to zonal mean)

from netCDF4 import Dataset
from lut_mapping import abbr2name, abbr2unit
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='input data file path')
parser.add_argument('-v', '--variable', type=str, 
										help='the variable to plot: press, temp, theta, rho, vlat, vlon, vel1')
parser.add_argument('-r', '--Rp', type=float,
                    help="""radius of the planet (m). The x2 axis will be adjusted to ratio
										to planet radius if specified.""")
parser.add_argument('-c', '--cutoff', type=int, default=0,
                    help="""the thickness of top and bottom boundaries, measured in number
                    of layers. Used for plotting in 3 atmospheric sections: top, middle,
                    bottom""")
args = parser.parse_args()

# time slices for averaging
timeslices = slice(-100, None)
"""  examples
timeslices = slice(-100, None)   # Access the last 100 time slices
timeslices = slice(100, 120)     # Access time slices from 100 to 119
timeslices = [20]                # Access a specific time slice
timeslices = slice(None)         # Access all time slices
"""

# read the data
dataset = Dataset(args.data,'r')
time = dataset.variables['time'][timeslices]
x2 = dataset.variables['x2'][:]
x1 = dataset.variables['x1'][:]
var = dataset.variables[args.variable][timeslices]

# set parameters
x1_surface = args.Rp
x1_top = 12010.e3     # m

# set grids
Y, Z = x2/args.Rp, (x1-x1_surface)/(x1_top-x1_surface)

# average data over time and x3 axis
x3mean_var = np.mean(var[:,:,:,:], axis=(0,3))
print(f"# {len(time)} time slices averaged: {time}")

if args.cutoff == 0:  # plot without layer cutoff
	
	print(f"# plotting x3-mean {abbr2name[args.variable]} ...")

	# Create a figure
	plt.figure(figsize=(10, 6))

	# Plot contourf
	if args.variable in ['vel1', 'vel2', 'vel3']:
		ctf = plt.contourf(Y, Z, x3mean_var, 80, cmap='RdBu_r',
													 norm=TwoSlopeNorm(vmin=np.min(x3mean_var), vcenter=0, vmax=np.max(x3mean_var)))
	else:
		ctf = plt.contourf(Y, Z, x3mean_var, 80, cmap='RdBu_r',
													 vmin=np.min(x3mean_var), vmax=np.max(x3mean_var))

	cb = plt.colorbar(ctf)
	cb.set_label(f'{abbr2name[args.variable]} / {abbr2unit[args.variable]}', fontsize=15)

	# Labels and title
	plt.xlabel(f'$x_2$ / $R_p$', size=15)
	plt.ylabel('Normalized Height', size=15)
	#plt.title('')

	plt.savefig(f"../x3-mean_{args.variable}.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
	plt.close()

else:     # plot with layer cutoff
	
	print(f"# plotting x3-mean {abbr2name[args.variable]} with stretched bottom and top boundary...")

	cutoff = args.cutoff                # x1 cutoff
	Z_bb = Z[:cutoff]                   # x1 bottom boundary
	Z_m = Z[cutoff-1:-cutoff+1]         # x1 medium part
	Z_tb = Z[-cutoff:]                  # x1 top boundary

	x3mean_var_bb = x3mean_var[:cutoff,:]
	x3mean_var_m = x3mean_var[cutoff-1:-cutoff+1,:]
	x3mean_var_tb = x3mean_var[-cutoff:,:]

	# Plot contourf
	fig, axs = plt.subplots(3,1,figsize=(10, 10))

	ctf2 = axs[2].contourf(Y, Z_bb, x3mean_var_bb, 10, cmap='RdBu_r')
	plt.colorbar(ctf2)

	ctf1 = axs[1].contourf(Y, Z_m, x3mean_var_m, 50, cmap='RdBu_r')
	cb1 = plt.colorbar(ctf1)
	cb1.set_label(f'{abbr2name[args.variable]} / {abbr2unit[args.variable]}', fontsize=15)

	ctf0 = axs[0].contourf(Y, Z_tb, x3mean_var_tb, 10, cmap='RdBu_r')
	plt.colorbar(ctf0)

	# Labels and title
	plt.xlabel(f'x2 / $R_p$', size=15)
	axs[1].set_ylabel('Normalized Height', size=15)
	
	plt.savefig(f"../x3-mean_{args.variable}_stretched.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
	plt.close()

