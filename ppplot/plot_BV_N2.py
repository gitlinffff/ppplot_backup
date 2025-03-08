# Coordinate system: Polar
# Data dimensions: time x1 lat lon
# plot zonal mean Brunt-Vaisala frequency N^2
# Reference: "On the Linear Theory of the Land and Sea Breeze (Richard Rotunno, 1983)"

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='input data file path')
args = parser.parse_args()

"""User specify"""
# time slices for averaging
#timeslices = range(54)     # average 0-53
#timeslices = range(35,50)  # average 35-49
#timeslices = [-1]           # Instantaneous at -1
timeslices = []             # all time slices

# parameters
g = 22.3 
theta0 = 2000.
"""============"""

# read the data
dataset = Dataset(args.data,'r')
lat = dataset.variables['lat'][:]
x1 = dataset.variables['x1'][:]/1e3   # km
theta = dataset.variables['theta'][:]

# average data
if not timeslices:
  zonal_mean_theta = np.mean(theta[:,:,:,:], axis=(0,3))
  print("# all time slices averaged")
else:
  zonal_mean_theta = np.mean(theta[timeslices,:,:,:], axis=(0,3))
  print("# time slices averaged:", list(timeslices))

# calculate Brunt-Vaisala frequency N^2
shifted_theta = np.roll(zonal_mean_theta, 1, axis=0)
shifted_x1 = np.roll(x1, 1)
BV_N2 = ((zonal_mean_theta - shifted_theta) / (x1 - shifted_x1)[:, np.newaxis] * g / theta0)[1:]

x1_ = x1[:-1]

# Create a figure and a set of subplots
fig, axs = plt.subplots(3,1,figsize=(10, 10))

# Create a pseudocolor plot with a non-regular rectangular grid
#pc = plt.pcolor(lat, x1[2:63], BV_N2, shading='auto', cmap='RdBu_r', vmin=-np.max(np.abs(BV_N2)), vmax=np.max(np.abs(BV_N2)))
#plt.colorbar(pc, label='Brunt-Vasala frequency $N^2$ ($s^{-2}$)')

# Plot contour
cutoff = 6                             # x1 cutoff
x1_bb = x1_[:cutoff]                   # x1 bottom boundary
x1_m = x1_[cutoff-1:-cutoff+1]         # x1 medium part
x1_tb = x1_[-cutoff:]                  # x1 top boundary

BV_N2_bb = BV_N2[:cutoff,:]          # N2 bottom boundary
BV_N2_m = BV_N2[cutoff-1:-cutoff+1,:]    # N2 medium part
BV_N2_tb = BV_N2[-cutoff:,:]         # N2 top boundary

contour2 = axs[2].contourf(lat, x1_bb, BV_N2_bb, 150, cmap='RdBu_r',
											 vmin=-np.max(np.abs(BV_N2_bb)), vmax=np.max(np.abs(BV_N2_bb)))
plt.colorbar(contour2, label='Brunt-Vasala frequency $N^2$ ($s^{-2}$)')

contour1 = axs[1].contourf(lat, x1_m, BV_N2_m, 150, cmap='RdBu_r',
											 vmin=-np.max(np.abs(BV_N2_m)), vmax=np.max(np.abs(BV_N2_m)))
plt.colorbar(contour1, label='Brunt-Vasala frequency $N^2$ ($s^{-2}$)')

contour0 = axs[0].contourf(lat, x1_tb, BV_N2_tb, 150, cmap='RdBu_r',
											 vmin=-np.max(np.abs(BV_N2_tb)), vmax=np.max(np.abs(BV_N2_tb)))
plt.colorbar(contour0, label='Brunt-Vasala frequency $N^2$ ($s^{-2}$)')

# Labels and title
plt.xlabel('Latitude', size=15)
axs[1].set_ylabel('Height / km', size=15)
#plt.title('')

plt.savefig("../Brunt-Vasala_frequency_N2.png",dpi=300)
