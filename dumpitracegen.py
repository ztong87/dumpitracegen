#!/usr/bin/env python
# DUMPI Trace Generator

import argparse

import traffic      # traffic functions
import simpleconfig # code for config file parsing
import asciimpi     # ASCII MPI DUMPI strings

# Takes in the ranks of a job
# returns {rank : [ranks talking to this rank]}
def receives(ranks):
    comms = {}
    for rank in ranks:
        comms[rank] = []

    for src, send in ranks.iteritems():
        for dst in send:
            comms[dst] += [src]  # add receives to destination ranks
    return comms

# takes traffic information and puts it into output files
def generate_dumpi(jobs, prefix, startwall = 100, init_dt = 1, dt = 1, finalize_dt = 1, verbose = False):
    if verbose:
        print 'Generating Traffic'

    job_traffic = simpleconfig.generate_traffic(jobs)

    if verbose:
        print 'Traffic Generate Completed. Writing to files ...'

    # get total number of ranks
    world_size = 0
    for _, ranks in job_traffic.iteritems():
        world_size += len(ranks)

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

    # generate the communications for each job
    file_count = 0
    for job_id, ranks in job_traffic.iteritems():
        for rank, incoming in receives(ranks).iteritems():
            # write ASCII data to file
            filename = prefix + '-' + str(rank)
            with open(filename + '.dumpi', 'w') as dumpi:
                line, startwall = asciimpi.MPI_Init(startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = asciimpi.MPI_Comm_rank(rank, 2, startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = asciimpi.MPI_Comm_size(2, world_size, startwall, init_dt)
                dumpi.write(line + '\n')

                for send in ranks[rank]:
                    line, startwall = asciimpi.MPI_Send(startwall, dt, jobs[job_id]['size'], 1, send, 0, 2, startwall, dt, 0)
                    dumpi.write(line + '\n')

                for recv in incoming:
                    line, startwall = asciimpi.MPI_Recv(startwall, dt, jobs[job_id]['size'], 1, recv, 0, 2, startwall, dt, 0)
                    dumpi.write(line + '\n')

                line, _ = asciimpi.MPI_Finalize(startwall, finalize_dt)
                dumpi.write(line + '\n')

            file_count += 1
            if verbose:
                print 'Wrote ' + filename + '.dumpi ({:3.2f}%)'.format(100. * file_count / world_size)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate Dumpi Traces with parameters')
    parser.add_argument('config',    type=str,                  help='file with list of job descriptions')
    parser.add_argument('prefix',    type=str,                  help='output file name prefix')
    parser.add_argument('-start',    type=float, default=100.0, help='starting walltime (default 100)')
    parser.add_argument('-init_dt',  type=float, default=1.0,   help='time to run init functions (default 1)')
    parser.add_argument('-dt',       type=float, default=1.0,   help='time to run functions (default 1)')
    parser.add_argument('-final_dt', type=float, default=1.0,   help='time to run finalize functions (default 1)')
    parser.add_argument('-v',        action='store_true',       help='If specified, prints progress message')
    args = parser.parse_args()

    generate_dumpi(simpleconfig.parse(args.config), args.prefix, args.start, args.init_dt, args.dt, args.final_dt, args.v)
