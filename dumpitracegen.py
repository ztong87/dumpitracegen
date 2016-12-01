#!/usr/bin/env python
# DUMPI Trace Generator

import argparse
import traffic  # traffic functions
import config   # codef for config file parsing

# takes traffic information and puts it into output files
def generate_dumpi(jobs, output, start_time = 100, mpi_init_dt = 1, mpi_dt = 1, mpi_finalize_dt = 1):
    for job, ranks in jobs.iteritems():
        for rank, traffic in ranks.iteritems():
            # reset offsets
            start = start_time
            init_dt = mpi_init_dt
            dt = mpi_dt
            final_dt = mpi_finalize_dt

            # write ASCII data to file
            filename = output + '-' + str(rank)
            with open(filename + '.dumpi', "w") as dumpi:
                # write header record
                # dumpi.write(header)

                # add mpi header
                dumpi.write("MPI_Initialized entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt
                dumpi.write("int result=0\n")
                dumpi.write("MPI_Initialized returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt

                dumpi.write("MPI_Initialized entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt
                dumpi.write("int result=0\n")
                dumpi.write("MPI_Initialized returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt

                dumpi.write("MPI_Init entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt
                dumpi.write("int argc=0\n")
                dumpi.write("string argv[0]=<IGNORED>\n")
                dumpi.write("MPI_Init returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt

                dumpi.write("MPI_Comm_rank entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt
                dumpi.write("MPI_Comm comm=2 (MPI_COMM_WORLD)\n")
                dumpi.write("int rank={}\n".format(rank))
                dumpi.write("MPI_Comm_rank returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt

                dumpi.write("MPI_Comm_size entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt
                dumpi.write("MPI_Comm comm=2 (MPI_COMM_WORLD)\n")
                dumpi.write("int size={}\n".format(len(ranks)))
                dumpi.write("MPI_Comm_size returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt

                dumpi.write("MPI_Comm_dup entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt
                dumpi.write("MPI_Comm oldcomm=2 (MPI_COMM_WORLD)\n")
                dumpi.write("MPI_Comm newcomm=4 (user-defined-comm)\n")
                dumpi.write("MPI_Comm_dup returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, init_dt)); start += init_dt

                # ##############################
                # write communication to trace #
                # ##############################

                # write mpi finalize
                dumpi.write("MPI_Finalize entering at walltime {}, cputime {} seconds in thread 0.\n".format(start, final_dt)); start += final_dt
                dumpi.write("MPI_Finalize returning at walltime {}, cputime {} seconds in thread 0.\n".format(start, final_dt));

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate Dumpi Traces with parameters')
    parser.add_argument('config',    type=str,                help='file with list of job descriptions')
    parser.add_argument('output',    type=str,                help='output file name')
    parser.add_argument('-start',    type=float, default=100, help='trace start time')
    parser.add_argument('-init_dt',  type=float, default=1,   help='time to run init functions')
    parser.add_argument('-dt',       type=float, default=1,   help='time to run functions')
    parser.add_argument('-final_dt', type=float, default=1,   help='time to run finalize functions')
    args = parser.parse_args()

    jobs = config.parse(args.config)
    if jobs:
        generate_dumpi(traffic.generate_traffic(jobs), args.output, args.start, args.init_dt, args.dt, args.final_dt)
    else:
        print 'No jobs found. Nothing done.'
