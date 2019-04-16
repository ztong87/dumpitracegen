# dumpitracegen

DUMPI Trace Generator

Generates synthetic traffic given some parameters
and writes ASCII DUMPI files to reflect the traffic.
.meta file is also written.

Prerequisites:
    Python 2 (2.7 or greater)

usage: dumpitracegen.py [-h] [--a2d A2D] [--start START] [--init_dt INIT_DT]
                        [--dt DT] [--final_dt FINAL_DT]
                        config prefix

positional arguments:
  config               file with list of job descriptions
  prefix               output filename prefix

optional arguments:
  -h, --help           show this help message and exit
  --a2d A2D            specify converter to convert ASCII output to binary
  --start START        starting walltime (default 100.0 seconds since epoch)
  --init_dt INIT_DT    time to run init functions (default 1.0 seconds)
  --dt DT              time to run MPI functions (default 1.0 seconds)
  --final_dt FINAL_DT  time to run finalize functions (default 1.0 seconds)

Note: All jobs start at the same time.

Adding new configuration file line parsers:
    Modify the function config.parse_line

    Default format:
        rank-start rank-end msg-count msg-type  iterations pattern pattern-specific-values
        ex:
            0         255     1024    MPI_CHAR       5      rand               1

Adding new traffic patterns:
    Add the traffic pattern.py file into the traffic directory.
        Input:
            Job dictionary from parser

            Fields that are already available:
                start rank
                end rank
                how many elements to send
                data type of elements
                number of iterations
                traffic pattern name

        Output
            {source rank : [destination ranks]}

    Add the traffic pattern into traffic/__init__.py
