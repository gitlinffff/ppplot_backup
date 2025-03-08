#!/bin/bash

# Remove files with certain pattern and file number larger than a certain value

# Loop over each file with the pattern "lava-thm.*.rst"
for file in lava-thm.*.rst; do
    # Extract the number from the filename
    number=$(echo "$file" | sed -n 's/lava-thm.0\([0-9]*\).rst/\1/p')

    # Check if the number is greater than 02693
    if [[ $number -gt 2693 ]]; then
        rm "$file"
    fi
done

