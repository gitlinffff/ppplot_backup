# Coordinate system: Polar
# Data dimensions: time x1 lat lon
# Description: plot z-theta profile at specified latitudes

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='input data file path')
args = parser.parse_args()

# time slices for averaging
#timeslices = range(54)     # average 0-53
#timeslices = range(35,50)  # average 35-49
#timeslices = [5]           # Instantaneous at 5
timeslices = []             # all time slices

lat_idx = [0,15,30,45,60,75,90]

# read the data
dataset = Dataset(args.data,'r')
time = dataset.variables['time'][:]
lat = dataset.variables['lat'][:]
x1 = dataset.variables['x1'][:]/1e3
temp = dataset.variables['temp'][:]
theta = dataset.variables['theta'][:]

# average data over time
if not timeslices:
	mean_theta = np.mean(theta[:,:,lat_idx,:], axis=(0,3))
	print("# all time slices averaged")
else:
	mean_theta = np.mean(theta[timeslices,:,lat_idx,:], axis=(0,3))
	print("# time slices averaged:", list(timeslices))

# plot z-theta
plt.figure(figsize=(8, 6))

for i in range(len(lat_idx)):
	plt.plot(mean_theta[:,i], x1, marker='o', ms=2, label = str(lat[lat_idx[i]]))

plt.xlim(1500,5000)
plt.legend()
plt.xlabel('Potential temperature / K', size=15)
plt.ylabel('Height / km', size=15)
plt.savefig("../z-theta_profile.png",dpi=300)
plt.close()
