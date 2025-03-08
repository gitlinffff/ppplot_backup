from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np


"""User specify"""
# The data should be in time-press-lat-lon dimensions
data_path = "pres_last10_lava-highres_main.nc"

# time slices for averaging
#timeslices = range(50)     # average 0-49
#timeslices = range(35,50)  # average 35-49
timeslices = [-1]           # Instantaneous at -1
"""============"""

# read the data
dataset = Dataset(data_path,'r')
time = dataset.variables['time'][:]
lat = dataset.variables['lat'][:]
lon = dataset.variables['lon'][:]
press = dataset.variables['press'][:]
temp = dataset.variables['temp'][:]
#vlat = dataset.variables['vlat'][:]
vlon = dataset.variables['vlon'][:]
vel1 = dataset.variables['vel1'][:]

# average data over time
mean_temp = np.mean(temp[timeslices,:,:,:], axis=0)
mean_vel1 = np.mean(vel1[timeslices,:,:,:], axis=0)
mean_vlon = np.mean(vlon[timeslices,:,:,:], axis=0)

zonal_mean_temp = np.mean(mean_temp, axis=2)
zonal_mean_vel1 = np.mean(mean_vel1, axis=2)
zonal_mean_vlon = np.mean(mean_vlon, axis=2)

print("# time slices averaged:", list(timeslices))

# Downsample the data
stride = 3 
press_downsampled = press[::stride]
lat_downsampled = lat[::stride]
vel1_downsampled = zonal_mean_vel1[::stride, ::stride]
vlon_downsampled = zonal_mean_vlon[::stride, ::stride]

# Calculate wind speed
#wind_speed = (mean_vlat**2 + mean_vlon**2)**0.5

# get the pressure at the isobaric plane
#pressure = press[press_idx]
#print(f"# isobaric plane {pressure} Pa")

# Create a figure and a set of subplots
plt.figure(figsize=(10, 6))

# Plot contour
#contour = plt.contour(lon, lat, data)
#plt.colorbar(contour, label='Temperature')

# Plot pcolor
pc = plt.pcolor(lat, press, zonal_mean_temp, shading='auto')
plt.colorbar(pc, label='Temperature')

# Plot the wind vectors with quiver
plt.quiver(lat_downsampled, press_downsampled, vlon_downsampled, vel1_downsampled, width=0.001, headwidth=5, headlength=7)

# Labels and title
plt.xlabel('Latitude')
plt.ylabel('Pressure')
plt.title(f'Zonal-mean wind field streamlines')

# Set the y-axis to a logarithmic scale
plt.yscale('log')

# Inverting the y-axis if pressure increases with depth/altitude
plt.gca().invert_yaxis()

plt.savefig(f"zonalmean_windvector_temp.png",dpi=300)
