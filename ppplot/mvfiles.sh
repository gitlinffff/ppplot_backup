#!/bin/bash

# Remove files with certain pattern and file number larger than a certain value

# Loop over each file with the pattern "lava-thm.*.rst"
for file in lava-3dcart.out*.*.nc; do
    # Extract the number from the filename
    number=$(echo "$file" | sed -n 's/.*\.0\([0-9]*\)\.nc/\1/p')
    
		# Remove leading zeros from the extracted number
    number=$(echo "$number" | sed 's/^0*//')
    
		# Check if the number is greater than 02693
    if [[ $number -gt 416 ]]; then
        mv "$file" "../out_section2/"
    fi
done

