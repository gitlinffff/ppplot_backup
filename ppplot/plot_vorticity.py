# Coordinate system: Cartesian
# Data dimensions: time x1 x2 x3
# Description: plot mean vorticity over timeslices on horizontal planes

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import TwoSlopeNorm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='input data file path')
args = parser.parse_args()

# time slices for averaging
timeslices = slice(-50, None)   # Access the last 100 time slices

lvls_to_plot = [45,31,17]  # select x1 levels in descending order 

Rp = 12000.e3   # planetary radius
x1_surface = Rp
x1_top = 12010.e3
omega = 9.87e-5

# Extract data
dataset = nc.Dataset(args.data)
time = dataset.variables['time'][timeslices]
u = dataset.variables['vel3'][timeslices]  # Shape (t, x1, x2, x3)
v = dataset.variables['vel2'][timeslices]  # Shape (t, x1, x2, x3)
x1 = dataset.variables['x1'][:]
x2 = dataset.variables['x2'][:]
x3 = dataset.variables['x3'][:]

# Modify these based on your actual spatial grid (if not uniform)
dx3 = x3[1] - x3[0]  # Define the grid spacing in the x3 direction
dx2 = x2[1] - x2[0]  # Define the grid spacing in the x2 direction

# Initialize an empty array
rel_vorticity = np.empty_like(u)

# Calculate relative vorticity: ζ = dv/dx - du/dy
for t in range(len(time)):  # Loop over time slices
	for level in range(len(x1)):  # Loop over altitude levels
		du_dy, du_dx = np.gradient(u[t, level, :, :], dx2, dx3)
		dv_dy, dv_dx = np.gradient(v[t, level, :, :], dx2, dx3)

		rel_vorticity[t, level, :, :] = dv_dx - du_dy

# Take the mean across the time axis
mean_time_rel_vorticity = np.mean(rel_vorticity, axis=0)  # Shape (x1, x2, x3)
print(f"# {len(time)} time slices averaged: day {time[0]/86400:.2f} to {time[-1]/86400:.2f}")

# rotation
f = 2 * omega * np.sin(x2/Rp)
f_extend3d = np.tile(f[np.newaxis, :, np.newaxis], (mean_time_rel_vorticity.shape[0], 1, mean_time_rel_vorticity.shape[2]))

# Calculate absolute vorticity
abs_vorticity = mean_time_rel_vorticity + f_extend3d

"""Plot 1: vorticity on horizontal planes"""
N_lvls = len(lvls_to_plot)
fig, axs = plt.subplots(N_lvls,2,figsize=(5*2, 3*N_lvls))
X, Y = x3/Rp, x2/Rp
ct_levels = 20   # number of countour levels
cmap = 'RdBu_r'

for i in range(N_lvls):
  
	rel_height = (x1[lvls_to_plot[i]]-x1_surface)/(x1_top-x1_surface)

	# axs(i,0)
	data = mean_time_rel_vorticity[lvls_to_plot[i]]
	ctf = axs[i,0].contourf(X, Y, data, ct_levels, cmap=cmap,
													#norm=TwoSlopeNorm(vmin=np.min(data), vcenter=0, vmax=np.max(data)))
													norm=TwoSlopeNorm(vmin=-1e-4, vcenter=0, vmax=1e-4))
	cb = fig.colorbar(ctf, ax=axs[i,0], label='')
	# Format the colorbar with scientific notation
	cb.formatter = ticker.ScalarFormatter(useMathText=True)  # Use scientific notation
	cb.formatter.set_powerlimits((0, 0))  # Force scientific notation
	cb.update_ticks()  # Update the colorbar with the new format

	# axs(i,1)
	data = abs_vorticity[lvls_to_plot[i]]
	ctf = axs[i,1].contourf(X, Y, data, ct_levels, cmap=cmap,
													#norm=TwoSlopeNorm(vmin=np.min(data), vcenter=0, vmax=np.max(data)))
													norm=TwoSlopeNorm(vmin=-1e-4, vcenter=0, vmax=1e-4))
	cb = fig.colorbar(ctf, ax=axs[i,1], label=f'Normalized Height {rel_height}')
	# Format the colorbar with scientific notation
	cb.formatter = ticker.ScalarFormatter(useMathText=True)  # Use scientific notation
	cb.formatter.set_powerlimits((0, 0))  # Force scientific notation
	cb.update_ticks()  # Update the colorbar with the new format

axs[0,0].set_title('Relative Vorticity',fontsize=14)
axs[0,1].set_title('Absolute Vorticity',fontsize=14)

# Add x and y labels for the entire figure
fig.text(0.5, 0.01, f'$x_{3}/R_p$', ha='center', va='center', fontsize=14)
fig.text(0.01, 0.5, f'$x_{2}/R_p$', ha='center', va='center', rotation='vertical', fontsize=14)

plt.tight_layout()
plt.savefig("../vorticity.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
plt.close()

""" Plot 2: zonal mean of horizontal plane vorticity """
rel_vorticity_yz = np.mean(mean_time_rel_vorticity, axis=2)  # Shape (x1, x2)
abs_vorticity_yz = np.mean(abs_vorticity, axis=2)            # Shape (x1, x2)

fig, axs = plt.subplots(1,2,figsize=(10, 3))
Y, Z = x2/Rp, (x1-x1_surface)/(x1_top-x1_surface)

for i,data in enumerate([rel_vorticity_yz,abs_vorticity_yz],0):
	ctf = axs[i].contourf(Y, Z, data, 30, cmap=cmap,
													norm=TwoSlopeNorm(vmin=-0.5e-4, vcenter=0, vmax=0.5e-4))
	cb = fig.colorbar(ctf, ax=axs[i], label='')
	# Format the colorbar with scientific notation
	cb.formatter = ticker.ScalarFormatter(useMathText=True)  # Use scientific notation
	cb.formatter.set_powerlimits((0, 0))  # Force scientific notation
	cb.update_ticks()  # Update the colorbar with the new format
	
	axs[i].set_xlabel(f'$x_{2}/R_p$  (Latitude)', fontsize=12)
	axs[i].set_xlim(-0.4, 0.4)

axs[0].set_ylabel(f'Normalized Height', fontsize=12)
axs[0].set_title('Relative Vorticity',fontsize=12)
axs[1].set_title('Absolute Vorticity',fontsize=12)

plt.tight_layout()
plt.savefig("../zonalmean_vorticity.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
plt.close()

""" Plot 3: vorticity with respect to y """
fig, axs = plt.subplots(1,2,figsize=(10, 3))
ftsize = 14
Y = x2/Rp

for lvl in lvls_to_plot:
	rel_height = (x1[lvl]-x1_surface)/(x1_top-x1_surface)
	
	axs[0].plot(Y, rel_vorticity_yz[lvl], label=f'{rel_height}')
	axs[1].plot(Y, abs_vorticity_yz[lvl], label=f'{rel_height}')

# Add dashed horizontal lines at y=0
axs[0].axhline(0, color='black', linestyle='--', linewidth=0.8)
axs[1].axhline(0, color='black', linestyle='--', linewidth=0.8)

# scientific notation for y-axis
axs[0].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
axs[1].ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

# set axis limits
#axs[0].set_xlim(-0.4, 0.4)
#axs[1].set_xlim(-0.4, 0.4)
axs[0].set_ylim(-1e-4, 1e-4)
axs[1].set_ylim(-1e-4, 1e-4)

# set axis labels
axs[0].set_xlabel(f'$x_{2}/R_p$  (Latitude)', fontsize=ftsize)
axs[1].set_xlabel(f'$x_{2}/R_p$  (Latitude)', fontsize=ftsize)
axs[0].set_ylabel('Relative Vorticity',fontsize=ftsize)
axs[1].set_ylabel('Absolute Vorticity',fontsize=ftsize)

# set legends
axs[0].legend(title="Normalized Height", fontsize=8)
axs[1].legend(title="Normalized Height", fontsize=8)

plt.tight_layout()
plt.savefig("../vorticity_with_y.png",dpi=300,bbox_inches='tight',pad_inches=0.1)
plt.close()
