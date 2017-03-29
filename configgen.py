#!/usr/bin/env python
# Generate a set of configuration files for dumpitracege.py
# input: numRanks, pattern, datatype, pattern_var, num_iter
# output: configuration files with the following foramt
#   start_rank, end_rank,   size,   datatype,  num_iter     pattern,   pattern_var,    
#       0       nunRanks-1  1000     MPI_INT      1         shift          8 

import os 
import sys 
import subprocess

# Generate traffic for one flow
# Write into output file with flows in the dumpitrace format
# configline: list of paramester to be written into the output file
# outfile: file header for the configuration
def write_file(configline, outfile):
    #print subprocess.check_output(['rm', outfile])
    #subproces.call('rm outfile')

    with open(outfile, 'w') as file:
        file.write(configline)

if __name__ == '__main__':

    # Generate the configuration files based on the a set of attributes
    # pattern = "shift_right"
    # ranks: 0 to num_ranks-1
    # dataytpe = MPI_INT
    # size = 100000000

    #pattern_var = [26, 43, 55]
    #num_ranks = 64
    #num_iter = 1
    #size = 100000000

    pattern_var = [230, 513, 790]
    num_ranks = 1024
    num_iter = 1
    size = 100000000


    for i in pattern_var:
        outfile = "shift"
        outfile += str(str(i)) + "-"
        outfile += str(num_ranks) + "ranks-"
        outfile += str(num_iter) + "iter"
        #print outfile 
        
        configline = "0 "+ " "
        configline += str(num_ranks - 1) + " "
        configline += str(size) + " "
        configline += str("MPI_INT") + " "
        configline += str(num_iter) + " "
        configline += str("shift_right") + " "
        configline += str(i)+ " " 
        configline += "\n"
        #print configline 

        # Wr1ite the output flows into file
        write_file(configline, outfile)

    # The outut of "ls -al" is returned from a seperate subprocess
    print subprocess.check_output(['ls','-l'])
    
    # Call dumpitracegen.py to generate the DUMPI traces 
    



