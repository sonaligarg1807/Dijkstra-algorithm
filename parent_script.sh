#!/bin/bash

# Function to get user input for source resid and cutoff distance
get_user_input() {
    echo "Enter the source resid:"
    read source_resid
    echo "Enter the cutoff distance:"
    read cutoff_distance
}

# Get user input for source resid and cutoff distance for the first time
get_user_input

# Initialize a set to keep track of visited source resids
visited_source_resids=()

while true; do
    # Check if the source resid has already been visited
    if [[ " ${visited_source_resids[@]} " =~ " ${source_resid} " ]]; then
        echo "Source resid $source_resid has already been visited. Exiting."
        exit 0
    fi

    # Add the current source resid to the visited set
    visited_source_resids+=("$source_resid")

    # Step 1: Run weights_source_resid.py with the source resid and cutoff distance
    echo "Running weights_source_resid.py with source_resid=$source_resid and cutoff_distance=$cutoff_distance"
    python3 weights_source_resid.py $source_resid $cutoff_distance

    # Check if the first script ran successfully
    if [ $? -ne 0 ]; then
        echo "weights_source_resid.py failed. Exiting."
        exit 1
    fi

    # Step 2: Run test1_dj.py
    echo "Running test1_dj.py"
    python3 test1_dj.py

    # Check if the second script ran successfully
    if [ $? -ne 0 ]; then
        echo "test1_dj.py failed. Exiting."
        exit 1
    fi

    # Extract the new source resid from output_path.txt
    source_resid=$(tail -n 1 output_path.txt | awk '{print $1}')
done

echo "All tasks completed."