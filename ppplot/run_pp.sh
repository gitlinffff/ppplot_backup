#!/bin/bash
# Description: plot z-theta profile

# Define the log file
LOG_FILE="../ppexec.log"

# Clear the log file at the beginning of the script
> $LOG_FILE

original_input="../lava-thermal_conduct-a1-main.nc"

# Step 1: Extract the last 5 slices of the 'time' dimension
echo "# Starting ncks operation..." | tee -a $LOG_FILE
output1="${original_input/.nc/_last5.nc}"
ncks -d time,-5,,1 "$original_input" "$output1" 2>&1 | tee -a $LOG_FILE
echo "# ncks operation completed." | tee -a $LOG_FILE

# Step 2: Convert to polar coordinates
echo "# Starting conversion to polar coordinates..." | tee -a $LOG_FILE
output2="${output1/main/polar}"
python convert_to_polar.py "$output1" -o "$output2" 2>&1 | tee -a $LOG_FILE
echo "# Conversion to polar coordinates completed." | tee -a $LOG_FILE

# Step 3: Plot z-theta profile
echo "# Starting plot of z-theta profile..." | tee -a $LOG_FILE
python plot_ztheta.py "$output2" 2>&1 | tee -a $LOG_FILE
echo "# Plotting completed." | tee -a $LOG_FILE

echo "# All processes completed successfully." | tee -a $LOG_FILE


