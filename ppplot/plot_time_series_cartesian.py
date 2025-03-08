# Coordinate system: 3D cartesian
# Data dimensions: time x1 x2 x3
# Description: Plot the time series of the x3-mean of a variable

from netCDF4 import Dataset
from lut_mapping import abbr2name, abbr2unit
import matplotlib.pyplot as plt
import numpy as np

"""User specify"""
data_path = "../lava-3dcart-b1-main.nc"

variable = "theta"
x1 = 0                 # height index
surface_height = 12000. # km
"""============"""

# read the data
with Dataset(data_path, 'r') as dataset:
	time = dataset.variables['time'][:]
	x2 = dataset.variables['x2'][:]/1e3  # km
	height = dataset.variables['x1'][x1]/1e3 - surface_height   # km
	var = dataset.variables[variable][:]

var_t_x2 = np.mean(var[:,x1,:,:], axis=2)

# first plot -- pcolor for all x2
plt.figure(figsize=(10, 6))

pc = plt.pcolor(time, x2, var_t_x2.T, shading='nearest')
plt.colorbar(pc, label=f'{abbr2name[variable]} / {abbr2unit[variable]}')
plt.xlabel('time / s',size=15)
plt.ylabel('x2 / km')
plt.title(f'Time series of x3-mean {abbr2name[variable]} at height {height:.2f} km')

plt.savefig(f"../{variable}_h{x1}_time_series.png",dpi=300)
plt.close()

# second plot -- line chart for specified x2
plt.figure(figsize=(10, 6))

ix2_N = -3
ix2_S = 2
var_N = var_t_x2[:,ix2_N]
var_S = var_t_x2[:,ix2_S]
plt.plot(time, var_N, marker='o', ms=2, label = f'{x2[ix2_N]} km')
plt.plot(time, var_S, marker='o', ms=2, label = f'{x2[ix2_S]} km')
plt.xlabel('time / s',size=15)
plt.ylabel(f'{abbr2name[variable]} / {abbr2unit[variable]}',size=15)
plt.legend(title=f'$x_{2}$')
plt.title(f'Time series of x3-mean {abbr2name[variable]} at height {height:.2f} km',size=15)

plt.savefig(f"../{variable}_h{x1}_time_series_x2.png",dpi=300)
plt.close()
