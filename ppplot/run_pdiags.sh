#!/bin/bash
# Description: plot_x3mean_var.py  for multiple variables

# input data
data="../lava-3dcart-e1-2-main.nc"

# Define the log file
LOG_FILE="../pdiags.log"

# Clear the log file at the beginning of the script
> $LOG_FILE

# plotting
python plot_x3mean_var.py "$data" -v theta -r 12000000. 2>&1 | tee -a $LOG_FILE
python plot_x3mean_var.py "$data" -v temp  -r 12000000. 2>&1 | tee -a $LOG_FILE
python plot_x3mean_var.py "$data" -v vel1  -r 12000000. 2>&1 | tee -a $LOG_FILE
python plot_x3mean_var.py "$data" -v vel2  -r 12000000. 2>&1 | tee -a $LOG_FILE
python plot_x3mean_var.py "$data" -v vel3  -r 12000000. 2>&1 | tee -a $LOG_FILE

echo "# All plotting completed successfully." | tee -a $LOG_FILE


