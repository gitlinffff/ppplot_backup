# Coordinate system: Polar
# Data dimensions: time x1 lat lon
# Description: plot zonal-mean z-gradient of a variable

from netCDF4 import Dataset
from lut_mapping import abbr2name, abbr2unit 
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='input data file path')
parser.add_argument('-v', '--variable', type=str, 
										help='the variable to plot: press, temp, theta, rho, vlat, vlon, vel1')
parser.add_argument('-c', '--cutoff', type=int, default=0,
										help="""the thickness of top and bottom boundaries, measured in number
										of layers. Used for plotting in 3 atmospheric sections: top, middle,
										bottom""")
args = parser.parse_args()


# time slices for averaging
#timeslices = range(50)     # average 0-49
#timeslices = range(35,50)  # average 35-49
#timeslices = [-1]          # Instantaneous at -1
timeslices = []             # all time slices

# read the data
dataset = Dataset(args.data,'r')
lat = dataset.variables['lat'][:]
x1 = dataset.variables['x1'][:]/1e3   # km
var = dataset.variables[args.variable][:]
print(f"# plotting zonal-mean {abbr2name[args.variable]} z-gradient ...")

# average data
if not timeslices:
	zonal_mean_var = np.mean(var[:,:,:,:], axis=(0,3))
	print("# all time slices averaged")
else:
	zonal_mean_var = np.mean(var[timeslices,:,:,:], axis=(0,3))
	print("# time slices averaged:", list(timeslices))

# calculate z-gradient of the variable
shifted_var = np.roll(zonal_mean_var, 1, axis=0)
shifted_x1 = np.roll(x1, 1)
var_zgrad = ((zonal_mean_var - shifted_var) / (x1 - shifted_x1)[:, np.newaxis])[1:]

x1_ = x1[:-1]


if args.cutoff == 0:
	# Create a figure
	plt.figure(figsize=(10, 6))

	# Plot pcolor
	#pc = plt.pcolor(lat, x1[2:63], BV_N2, shading='auto', cmap='RdBu_r', vmin=-np.max(np.abs(BV_N2)), vmax=np.max(np.abs(BV_N2)))
	#plt.colorbar(pc, label='Brunt-Vasala frequency $N^2$ ($s^{-2}$)')

	# Plot contour
	ctf = plt.contourf(lat, x1_, var_zgrad, 80, cmap='RdBu_r',
												 vmin=-np.max(np.abs(var_zgrad)), vmax=np.max(np.abs(var_zgrad)))
	cb = plt.colorbar(ctf)
	cb.set_label(f'z-gradient of {abbr2name[args.variable]}', fontsize=15)

	# Labels and title
	plt.xlabel('Latitude', size=15)
	plt.ylabel('Height / km', size=15)
	#plt.title('')

	plt.savefig(f"../zonalmean_{args.variable}_zgrad.png",dpi=300)

else:
	cutoff = args.cutoff                   # x1 cutoff
	x1_bb = x1_[:cutoff]                   # x1 bottom boundary
	x1_m = x1_[cutoff-1:-cutoff+1]             # x1 middle part
	x1_tb = x1_[-cutoff:]                  # x1 top boundary

	var_zgrad_bb = var_zgrad[:cutoff,:]          # data bottom boundary
	var_zgrad_m = var_zgrad[cutoff-1:-cutoff+1,:]    # data middle part
	var_zgrad_tb = var_zgrad[-cutoff:,:]         # data top boundary

	# Create a figure and a set of subplots
	fig, axs = plt.subplots(3,1,figsize=(10, 10))

	contour2 = axs[2].contourf(lat, x1_bb, var_zgrad_bb, 10, cmap='RdBu_r',
												 vmin=-np.max(np.abs(var_zgrad_bb)), vmax=np.max(np.abs(var_zgrad_bb)))
	plt.colorbar(contour2, label=f'z-gradient of {abbr2name[args.variable]}')

	contour1 = axs[1].contourf(lat, x1_m, var_zgrad_m, 50, cmap='RdBu_r',
												 vmin=-np.max(np.abs(var_zgrad_m)), vmax=np.max(np.abs(var_zgrad_m)))
	plt.colorbar(contour1, label=f'z-gradient of {abbr2name[args.variable]}')

	contour0 = axs[0].contourf(lat, x1_tb, var_zgrad_tb, 10, cmap='RdBu_r',
												 vmin=-np.max(np.abs(var_zgrad_tb)), vmax=np.max(np.abs(var_zgrad_tb)))
	plt.colorbar(contour0, label=f'z-gradient of {abbr2name[args.variable]}')

	# Labels and title
	plt.xlabel('Latitude', size=15)
	axs[1].set_ylabel('Height / km', size=15)
	#plt.title('')

	plt.savefig(f"../zonalmean_{args.variable}_zgrad_3p.png",dpi=300)
