# Coordinate system: Polar
# Data dimensions: time x1 lat lon
# Description: plot zonal-mean variable

from netCDF4 import Dataset
from lut_mapping import abbr2name, abbr2unit 
from matplotlib.colors import TwoSlopeNorm
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='input data file path')
parser.add_argument('-v', '--variable', type=str, 
										help='the variable to plot: press, temp, theta, rho, vlat, vlon, vel1')
args = parser.parse_args()

# time slices for averaging
timeslices = slice(None)
"""  examples
timeslices = slice(-100, None)   # Access the last 100 time slices
timeslices = slice(100, 120)     # Access time slices from 100 to 119
timeslices = [20]                # Access a specific time slice
timeslices = slice(None)         # Access all time slices
"""

# read the data
dataset = Dataset(args.data,'r')
time = dataset.variables['time'][timeslices]
x1 = dataset.variables['x1'][:] / 1.e3
lat = dataset.variables['lat'][:]
var = dataset.variables[args.variable][timeslices]
print(f"# plotting zonal-mean {abbr2name[args.variable]} ...")

# average data
zonal_mean_var = np.mean(var[:,:,:,:], axis=(0,3))
print(f"# {len(time)} time slices averaged: {time}")

# Create a figure
plt.figure(figsize=(10, 6))

# Plot contourf
if args.variable in ['vel1', 'vlat', 'vlon']:
	ctf = plt.contourf(lat, x1, zonal_mean_var, 80, cmap='RdBu_r',
		norm=TwoSlopeNorm(vmin=np.min(zonal_mean_var), vcenter=0, vmax=np.max(zonal_mean_var)))
	
	# mean value contour line
	contour0 = plt.contour(lat, x1, zonal_mean_var, levels=[0], colors='k', linewidths=.5)
	plt.clabel(contour0, fmt='0', fontsize=8, colors='k')

else:
	mean_value = np.mean(zonal_mean_var)
	ctf = plt.contourf(lat, x1, zonal_mean_var, 80, cmap='RdYlBu_r',
		norm=TwoSlopeNorm(vmin=np.min(zonal_mean_var), vcenter=mean_value, vmax=np.max(zonal_mean_var)))
	
	# mean value contour line
	contour0 = plt.contour(lat, x1, zonal_mean_var, levels=[mean_value], colors='k', linewidths=.5)
	plt.clabel(contour0, fmt=f'{mean_value:.1f}', fontsize=8, colors='k')

cb = plt.colorbar(ctf)
cb.set_label(f'{abbr2name[args.variable]} / {abbr2unit[args.variable]}', fontsize=15)
#cb.ax.text(1.6, 1.02, f'+{mean_value:.1f}', ha='center', va='bottom', transform=cb.ax.transAxes)

# Labels and title
plt.xlabel('Latitude',size=15)
plt.ylabel('Height / km', size=15)
plt.title(f'Zonal-mean {abbr2name[args.variable]}',size=15)

plt.savefig(f"../zonalmean_{args.variable}.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
plt.close()
