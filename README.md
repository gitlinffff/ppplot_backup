# Visualization and Plotting Instructions
Lateast modification: 3/8/2025
linfel@umich.edu

PPPlot is a collection of post-processing and visualization scripts designed to efficiently analyze and visualize scientific data.This repository is intended to streamline the workflow for climate science, planetary research, or other computational models requiring data interpretation.

# Features

- Flexible data post-processing functions.
- Customizable plotting utilities for high-quality scientific visuals.
- Efficient handling of NetCDF data, binary files, and other scientific data formats.
- Clear structure to integrate with existing research workflows.

# Requirements
- Python 3.x
- NumPy
- Matplotlib

# Usage
To plot zonal-mean variables such as temperature, pressure, density, velocity in beta-plane Cartesian settings:
```
python plot_x3mean_var.py your_netcdf_data.nc -v theta -r 12000000.
```
To plot zonal-mean variables in Cubed Sphere Exo3 settings:
```
python plot_zonalmean_var.py your_netcdf_data.nc -v theta
```

