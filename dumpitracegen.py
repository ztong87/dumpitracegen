#!/usr/bin/env python
# DUMPI Trace Generator

import argparse
import itertools
import random

# ###################################################################
#
# Traffic functions generate traffic for all ranks at the same time
#   Input:
#     start = first rank
#     end = last rank
#     n = times to run generator before pulling output
#     iterations = number of communications from each rank
#
#   Output
#    {job id : {source rank: [destination ranks]}
#
# ###################################################################

# generate all combinations; skip n indicies; get sd pair
# this is wrong
def perm(start, end, n, iterations):
    traffic = {rank : [] for rank in xrange(start, end + 1)}
    perms   = {rank : [] for rank in xrange(start, end + 1)}

    total_iterations = iterations * (end - start + 1)
    while total_iterations > 0:
        for src in xrange(start, end + 1):
            while not len(perms[src]):
                # generate more values
                for s, d in itertools.combinations(xrange(start, end), 2):
                    perms[s] += [d]

            if len(perms[src]) > n:
                if len(traffic[src]) < iterations:
                    traffic[src] += [perms[src][n]]  # read nth value
                    perms[src] = perms[src][n + 1:]  # 'pop front'
                    total_iterations -= 1
    return traffic

# shift right by n, with wrap around
def shift(start, end, n, iterations):
    traffic = {}
    for src in xrange(start, end + 1):
        dst = src + (n % (start - end + 1))
        if dst > end:
            dst -= start
        traffic[src] = [dst] * iterations
    return traffic

# generate n rounds before returning a random destination
def rand(start, end, n, iterations):
    # helper function
    def rng(start, end, src, n):
        for _ in xrange(n):
            random.randint(start, end)

        dst = random.randint(start, end)

        # keep generating until not talking to self
        while dst == src:
            dst = random.randint(start, end)

        return dst

    traffic = {}
    for src in xrange(start, end + 1):
        traffic[src] = [rng(start, end, src, n) for _ in xrange(iterations)]
    return traffic

# dictionary of traffic patterns to functions
TRAFFIC_PATTERNS = {
    'perm'        : perm,
    'permutation' : perm,
    'shift'       : shift,
    'rand'        : rand,
    'random'      : rand,
}

# returns {job id : {rank : [dst]}}
def generate_traffic(config):
    jobs = {}
    job_counter = 0
    for start, end, num_dst, size, iterations, pattern, count in config:
        # does not check for rank overlap
        jobs[job_counter] = TRAFFIC_PATTERNS[pattern](start, end, count, iterations)
        job_counter += 1
    return jobs

# takes traffic information and puts it into output files
def generate_dumpi(jobs, output, start_time = 100, mpi_init_dt = 1, mpi_dt = 1, mpi_finalize_dt = 1):
    for job, ranks in jobs.iteritems():
        for rank, traffic in ranks.iteritems():
            # reset offsets
            start = start_time
            init_dt = mpi_init_dt
            dt = mpi_dt
            final_dt = mpi_finalize_dt
            '''
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
            '''

# read in configuration file
# formatted as lines of
#    rank-start rank-end number-of-destinations msg-size iterations pattern count
#
# ex:
#        0         255           3                1024       5       perm    1
def read_config_file(filename):
    with open(filename, 'r') as config:
        jobs = []
        for line in config.readlines():
            # really simple parse
            line = line.split()
            if len(line):
                jobs += [[int(field) for field in line[:5]] + [line[5], int(line[6])]]
        return jobs if len(jobs) else None
    return None

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate Dumpi Traces with parameters')
    parser.add_argument('config',    type=str,                help='file with list of job descriptions')
    parser.add_argument('output',    type=str,                help='output file name')
    parser.add_argument('-start',    type=float, default=100, help='trace start time')
    parser.add_argument('-init_dt',  type=float, default=1,   help='time to run init functions')
    parser.add_argument('-dt',       type=float, default=1,   help='time to run functions')
    parser.add_argument('-final_dt', type=float, default=1,   help='time to run finalize functions')
    args = parser.parse_args()

    jobs = read_config_file(args.config)
    if jobs:
        generate_dumpi(generate_traffic(jobs), args.output, args.start, args.init_dt, args.dt, args.final_dt)
    else:
        print 'No jobs found. Nothing done.'
