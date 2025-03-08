# Description: Calculate the streamfunction on x1-x2 plane, and save it to a
#							 new .nc file together with the original variables.
# dPsi = vdz-wdy    dPsi = v2dx1-v1dx2
# The input file has to be Cartesian coordinate

import netCDF4 as nc
import numpy as np
#from scipy.interpolate import interp1d
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infile', type=str,
                    help='path to input file')
parser.add_argument('-o', '--outfile', type=str,
                    help='path to output file')
args = parser.parse_args()

# Read the dimensions
with nc.Dataset(args.infile, "r") as src:
	t_dim = src.dimensions["time"]
	x2 = src.variables["x2"][:]
	x3 = src.dimensions["x3"]
	x1 = src.variables["x1"][:]
	psi = np.zeros((len(t_dim), len(x1), len(x2), len(x3)))
	vel1 = src.variables["vel1"][:]
	vel2 = src.variables["vel2"][:]
	
	for i in range(1, len(x1)):
		psi[:, i, :, :] = psi[:, i - 1, :, :] + vel2[:, i, :, :] * (x1[i] - x1[i - 1])
	
	for j in range(1, len(x2)):
		psi[:, :, j, :] = psi[:, :, j - 1, :] - vel1[:, :, j, :] * (x2[j] - x2[j - 1])

with nc.Dataset(args.infile) as src, nc.Dataset(args.outfile, "w") as dst:
	# copy global attributes all at once via dictionary
	dst.setncatts(src.__dict__)
	# copy dimensions
	for name, dimension in src.dimensions.items():
			dst.createDimension(
					name, (len(dimension) if not dimension.isunlimited() else None)
			)
	# copy all file data except for the excluded
	for name, variable in src.variables.items():
			x = dst.createVariable(name, variable.datatype, variable.dimensions)
			dst[name][:] = src[name][:]
			# copy variable attributes all at once via dictionary
			dst[name].setncatts(src[name].__dict__)

	psi_var = dst.createVariable("psi", psi.dtype, ("time", "x1", "x2", "x3"))
	psi_var[:] = psi
	psi_var.units = "kg/s"
