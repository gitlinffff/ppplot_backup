# Coordinate system: Polar
# Data dimensions: time x1 lat lon
# Description: Plot the time series of the zonal-mean of a variable

from netCDF4 import Dataset
from lut_mapping import abbr2name, abbr2unit
import matplotlib.pyplot as plt
import numpy as np

"""User specify"""
data_path = "../lava-unif-a5-theta_polar.nc"

variable = "theta"
x1_idx = 31           # select x1 index
x1_surface = 12000.e3 # m
x1_top = 12010.e3     # m
"""============"""

# read the data
with Dataset(data_path, 'r') as dataset:
	time = dataset.variables['time'][:]
	lat = dataset.variables['lat'][:]
	x1 = dataset.variables['x1'][:]
	var = dataset.variables[variable][:]

normalized_h = (x1[x1_idx] - x1_surface) / (x1_top - x1_surface)
t_days = time/86400.
var_t_lat = np.mean(var[:,x1_idx,:,:], axis=2)

# first plot -- pcolor for all the latitudes
plt.figure(figsize=(10, 6))
ftsize = 15

pc = plt.pcolor(t_days, lat, var_t_lat.T, shading='nearest', cmap='RdBu_r')
cb = plt.colorbar(pc)
cb.set_label(f'{abbr2name[variable]} / {abbr2unit[variable]}', fontsize=ftsize)
plt.xlabel('time / days', size=ftsize)
plt.ylabel('Latitudes', size=ftsize)
plt.title(f'Time series of zonal-mean {abbr2name[variable]} at normalized height {normalized_h:.2f}')

plt.savefig(f"../{variable}_timeseries_h{normalized_h:.2f}.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
plt.close()

# second plot -- line chart for specified latitudes
plt.figure(figsize=(10, 6))

ilat_N = -3
ilat_S = 2
var_N = var_t_lat[:,ilat_N]
var_S = var_t_lat[:,ilat_S]
plt.plot(t_days, var_N, marker='o', ms=2, label = f'{lat[ilat_N]}')
plt.plot(t_days, var_S, marker='o', ms=2, label = f'{lat[ilat_S]}')
plt.xlabel('time / days',size=ftsize)
plt.ylabel(f'{abbr2name[variable]} / {abbr2unit[variable]}',size=ftsize)
plt.legend(title='Latitudes')
plt.title(f'Time series of zonal-mean {abbr2name[variable]} at normalized height {normalized_h:.2f} in polar regions',size=ftsize)

plt.savefig(f"../{variable}_timeseries_lat_h{normalized_h:.2f}.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
plt.close()
