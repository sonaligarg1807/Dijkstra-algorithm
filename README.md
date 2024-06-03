# Dijkstra-algorithm
This repository contains the scripts to find the path of largest coupling using Dijkstra algorithm
1. Just run the script 'parent_script.sh'. upon running 'parent_script.sh', enter the source_resid_index for example: 32 and cut-off distance = 0.25
2. This will start running 'extract_molecules.py' script which extracts the molecules from user entered source_resid within the specified cut-off distance. This creates an output file 'extracted.gro'
3. next it runs 'weights_source_resid.py' which calculates the average value of coupling between the source_resid and target_resid's present in 'extracted.gro' file and saves the output in 'average_coupling_values.txt'
4. then it runs 'test1_dj.py' which runs dijkstra algorithm to find the path of largest coupling using the weights from 'average_coupling_values.txt' file and it saves the output in 'output_path.txt' file.
5. It then updates the source_resid with the resid of the molecules with the largest coupling from the source and taking the same cutoff distance, it repeats the above process again.


Problems:
1. Dijkstra algorithm takes the negative value of weights as '0'
2. Dijkstra algorithm exits the code when it finds the new source_resid same as previous source_resid, which I am getting in case the coupling with other molecules is negative. 
   
