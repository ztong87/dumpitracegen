#!/usr/bin/env python
# DUMPI Trace Generator

import argparse
import os
import subprocess

import ASCII_DUMPI # ASCII DUMPI MPI functions to strings
import config      # handle configuration data
import traffic     # traffic functions

# Takes in {src rank : [[dst ranks]]}
# returns  {dst rank : [[src ranks]]}
def receives(ranks):
    recvs = {rank : [] for rank in ranks}

    # for each sender
    for src in ranks:
        # for each iteration
        iterations = ranks[src]
        for it in xrange(len(iterations)):
            for dst in iterations[it]:
                # if number of iterations dst has is too low
                while len(recvs[dst]) <= it:
                    recvs[dst] += [[]]

                # give destinaton this source at iteration it
                recvs[dst][it] += [src]
    return recvs

# takes traffic information and puts it into output files
def generate_dumpi(jobs, prefix, startwall, init_dt, dt, finalize_dt):
    # get total number of ranks
    world_size = 0
    for job in jobs:
        world_size += job['end'] - job['start'] + 1

    # write meta file
    with open(prefix + '.meta', 'w') as meta:
        meta.write('hostname=synthetic\n')
        meta.write('numprocs={}\n'.format(world_size))
        meta.write('username=firat.last\n')
        meta.write('startime={}\n'.format(int(startwall)))
        meta.write('fileprefix={}\n'.format(os.path.basename(prefix))) # if prefix ends in '/', prefix will be empty; prefix should not be a directory anyways
        meta.write('version=1\n')
        meta.write('subversion=1\n')
        meta.write('subsubversion=0\n')

    for job in jobs:
        # generate the sends for the current job
        ranks = config.generate_traffic(job)
        # generate the receives for the current job
        for rank, incoming in receives(ranks).iteritems():
            #########################################
            # should probably check for rank > 9999 #
            #########################################

            # write ASCII data to file
            filename = prefix + '-{:04d}'.format(rank)
            with open(filename, 'w') as dumpi:
                line, startwall = ASCII_DUMPI.MPI_Init(startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = ASCII_DUMPI.MPI_Comm_rank(rank, 2, startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = ASCII_DUMPI.MPI_Comm_size(2, world_size, startwall, init_dt)
                dumpi.write(line + '\n')

                # special case all to all traffic, calling MPI_Alltoall
                if 'MPI_Alltoall' == job['pattern']:
                    for it in xrange(job['iterations']):
                        line, startwall = ASCII_DUMPI.MPI_Alltoall(startwall,                               # start wall time
                                                                   dt,                                      # start cpu time
                                                                   job['count'],                            # number of elements
                                                                   ASCII_DUMPI.str_datatype[job['type']],   # type of element
                                                                   it,                                      # tag
                                                                   2,                                       # communicator
                                                                   startwall + dt,                          # end wall time
                                                                   dt,                                      # end cpu time
                                                                   0)
                        dumpi.write(line + '\n')
                else:
                    # make iterations of sends and receives the same size
                    while len(ranks[rank]) < len(incoming):
                        ranks[rank] += [[]]
                    while len(ranks[rank]) > len(incoming):
                        incoming += [[]]

                    # sends
                    for it in xrange(len(ranks[rank])):
                        for dst in ranks[rank][it]:
                            line, startwall = ASCII_DUMPI.MPI_Send(startwall,                               # start wall time
                                                                   dt,                                      # start cpu time
                                                                   job['count'],                            # number of elements
                                                                   ASCII_DUMPI.str_datatype[job['type']],   # type of element
                                                                   dst,                                     # destination rank
                                                                   it,                                      # tag
                                                                   2,                                       # communicator
                                                                   startwall + dt,                          # end wall time
                                                                   dt,                                      # end cpu time
                                                                   0)                                       # thread
                            dumpi.write(line + '\n')

                        # recieves
                        for src in incoming[it]:
                            line, startwall = ASCII_DUMPI.MPI_Recv(startwall,                               # start wall time
                                                                   dt,                                      # start cpu time
                                                                   job['count'],                            # number of elements
                                                                   ASCII_DUMPI.str_datatype[job['type']],   # type of element
                                                                   src,                                     # source rank
                                                                   it,                                      # tag
                                                                   2,                                       # communicator
                                                                   startwall + dt,                          # end wall time
                                                                   dt,                                      # end cpu time
                                                                   0)                                       # thread
                        dumpi.write(line + '\n')

                line, _ = ASCII_DUMPI.MPI_Finalize(startwall, finalize_dt)
                dumpi.write(line + '\n')

            # convert to binary
            if args.a2d:
                subprocess.call([args.a2d, filename, '-o', filename + '.bin'])

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Synthetic DUMPI Trace Generator')
    parser.add_argument('config',     type=str,                  help='name of file with list of job descriptions')
    parser.add_argument('prefix',     type=str,                  help='output filename prefix')
    parser.add_argument('--a2d',      type=str,   default=None,  help='specify converter to convert ASCII output to binary')
    parser.add_argument('--start',    type=float, default=100.0, help='starting walltime (default 100.0 seconds since epoch)')
    parser.add_argument('--init_dt',  type=float, default=1.0,   help='time to run init functions (default 1.0 seconds)')
    parser.add_argument('--dt',       type=float, default=1.0,   help='time to run MPI functions (default 1.0 seconds)')
    parser.add_argument('--final_dt', type=float, default=1.0,   help='time to run finalize functions (default 1.0 seconds)')
    args = parser.parse_args()

    generate_dumpi(config.parse(args.config), args.prefix, args.start, args.init_dt, args.dt, args.final_dt)
