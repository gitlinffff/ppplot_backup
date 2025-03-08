# Coordinate system: Cartesian or Polar (program will recognize)
# Data dimensions: (time x1 x2 x3) or (time x1 lat lon)
# Description: plot x3-mean or zonal-mean stream function

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data_path', type=str, help='input data file path')
args = parser.parse_args()

# time slices for averaging
timeslices = slice(None)
"""  examples
timeslices = slice(-100, None)   # Access the last 100 time slices
timeslices = slice(100, 120)     # Access time slices from 100 to 119
timeslices = [20]                # Access a specific time slice
timeslices = slice(None)         # Access all time slices
"""
lon_slices = []

Rp = 12000.e3      # m
x1_surface = Rp
x1_top = 12010.e3  # m
print(f'# Rp is set to {Rp} m.')

# read the data
with Dataset(args.data_path,'r') as dataset:
	time = dataset.variables['time'][timeslices]
	x1 = dataset.variables['x1'][:]                  # m
	psi = dataset.variables['psi'][timeslices]       # stream function
	var_names = dataset.variables.keys()

	if ('lat' in var_names) & ('x2' not in var_names):
		Y = dataset.variables['lat'][:]
		coorsys = "polar"
	elif ('x2' in var_names) & ('lat' not in var_names):
		Y = dataset.variables['x2'][:]/Rp        # ratio to Rp
		coorsys = "cart"
	else:
		raise Exception("check whether x2 or lat exist.")

# average data over time
mean_psi = np.mean(psi[:,:,:,:], axis=0)
print(f"# {len(time)} time slices averaged: {time}")

# then get zonal mean
if not lon_slices:
    zonal_mean_psi = np.mean(mean_psi[:,:,:], axis=2)
    print("# zonal mean along all longitudes")
else:
    zonal_mean_psi = np.mean(mean_psi[:,:,lon_slices], axis=2)
    print("# zonal mean along longitude slices", list(lon_slices))

# Create a figure
plt.figure(figsize=(10, 6))
fs = 12    # set common font size

Z = (x1-x1_surface)/(x1_top-x1_surface)
ctf = plt.contourf(Y, Z, zonal_mean_psi, 30)
cb = plt.colorbar(ctf)
cb.set_label('Stream Function', fontsize=fs)

# Labels and title
if coorsys == "polar":
	plt.xlabel('Latitude',size=fs)
elif coorsys == "cart":
	plt.xlabel(f'x2 / $R_p$',size=fs)
plt.ylabel('Normalized Height',size=fs)
plt.title(f'Zonal-mean wind field streamlines',size=fs+1)

plt.savefig(f"../streamfunction.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
