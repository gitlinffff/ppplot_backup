#!/bin/bash
# Description: plot x3-mean Psi

# Define the log file
LOG_FILE="../psi.log"

# Clear the log file at the beginning of the script
> $LOG_FILE

original_input="../lava-3dcart-e9-2-main.nc"
NUM_SLICES=50    # Define the number of slices you want from the end

# Step 1: Extract the last 5 slices of the 'time' dimension
echo "# Starting ncks operation..." | tee -a $LOG_FILE
output1="${original_input/.nc/_last${NUM_SLICES}.nc}"
ncks -d time,-"$NUM_SLICES",,1 "$original_input" "$output1" 2>&1 | tee -a "$LOG_FILE"
echo "# ncks operation completed." | tee -a $LOG_FILE

# Step 2: Calculate stream function and output a new .nc file
echo "# Starting calculating Psi..." | tee -a $LOG_FILE
output2="${output1/main/psi}"
python calculate_psi_cartesian.py -i "$output1" -o "$output2" 2>&1 | tee -a $LOG_FILE
echo "# Calculating Psi completed." | tee -a $LOG_FILE

# Step 3: Plot x3-mean Psi
echo "# Starting plot x3-mean Psi..." | tee -a $LOG_FILE
python plot_streamfunction.py "$output2" 2>&1 | tee -a $LOG_FILE
echo "# Plotting completed." | tee -a $LOG_FILE

echo "# All processes completed successfully." | tee -a $LOG_FILE


