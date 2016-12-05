#!/usr/bin/env python
# DUMPI Trace Generator

import argparse
import subprocess

import ASCII_DUMPI # ASCII DUMPI MPI functions to strings
import config      # handle configuration data
import traffic     # traffic functions

# Takes in {src rank : [dst ranks]}
# returns  {dst rank : [src ranks]}
def receives(ranks):
    comms = {}
    for rank in ranks:
        comms[rank] = []

    for src, send in ranks.iteritems():
        for dst in send:
            comms[dst] += [src]  # add receives to destination ranks
    return comms

# takes traffic information and puts it into output files
def generate_dumpi(jobs, prefix, startwall, init_dt, dt, finalize_dt):
    # get total number of ranks
    world_size = 0
    for job in jobs:
        world_size += job['end'] - job['start'] + 1

    # write meta file
    with open(prefix + '.meta', 'w') as meta:
        meta.write('hostname=\n')
        meta.write('numprocs={}\n'.format(world_size))
        meta.write('username=\n')
        meta.write('startime={}\n'.format(int(startwall)))
        meta.write('fileprefix={}\n'.format(prefix))
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

                for send in ranks[rank]:
                    line, startwall = ASCII_DUMPI.MPI_Send(startwall, dt, job['count'], ASCII_DUMPI.str_datatype[job['type']], send, 0, 2, startwall, dt, 0)
                    dumpi.write(line + '\n')

                for recv in incoming:
                    line, startwall = ASCII_DUMPI.MPI_Recv(startwall, dt, job['count'], ASCII_DUMPI.str_datatype[job['type']], recv, 0, 2, startwall, dt, 0)
                    dumpi.write(line + '\n')

                line, _ = ASCII_DUMPI.MPI_Finalize(startwall, finalize_dt)
                dumpi.write(line + '\n')

            # convert to binary
            if args.a2d:
                subprocess.call([args.a2d, filename, '-o', filename + '.bin'])

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate Synthetic Dumpi Traces')
    parser.add_argument('config',     type=str,                  help='file with list of job descriptions')
    parser.add_argument('prefix',     type=str,                  help='output filename prefix')
    parser.add_argument('--a2d',      type=str,   default=None,  help='define to convert ASCII output to binary')
    parser.add_argument('--start',    type=float, default=100.0, help='starting walltime (default 100.0 seconds since epoch)')
    parser.add_argument('--init_dt',  type=float, default=1.0,   help='time to run init functions (default 1.0 seconds)')
    parser.add_argument('--dt',       type=float, default=1.0,   help='time to run MPI functions (default 1.0 seconds)')
    parser.add_argument('--final_dt', type=float, default=1.0,   help='time to run finalize functions (default 1.0 seconds)')
    args = parser.parse_args()

    generate_dumpi(config.parse(args.config), args.prefix, args.start, args.init_dt, args.dt, args.final_dt)
