#!/usr/bin/env python
# DUMPI Trace Generator

import argparse

import traffic      # traffic functions
import simpleconfig # code for config file parsing
import asciimpi     # ASCII MPI DUMPI strings

# Takes in the ranks of a job
# returns { rank : [[sends], [recvs]]}
def communications(ranks):
    comms = {}
    for rank in ranks:
        comms[rank] = [[], []]

    for src, send in ranks.iteritems():
        comms[src][0] = send        # set list of ranks to communicate with
        for dst in send:
            comms[dst][1] += [src]  # add receives to destination ranks
    return comms

# takes traffic information and puts it into output files
def generate_dumpi(jobs, output, startwall = 100, init_dt = 1, dt = 1, finalize_dt = 1):
    job_traffic = simpleconfig.generate_traffic(jobs)

    # get total number of ranks
    world_size = 0
    for _, ranks in job_traffic.iteritems():
        world_size += len(ranks)

    # generate the communications for each job
    for job_id, ranks in job_traffic.iteritems():

        for rank, traffic in communications(ranks).iteritems():
            # write ASCII data to file
            filename = output + '-' + str(rank)
            with open(filename + '.dumpi', "w") as dumpi:
                # write header record

                # write MPI Init stuff ########################################
                line, startwall = asciimpi.MPI_Initialized(startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = asciimpi.MPI_Initialized(startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = asciimpi.MPI_Init(startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = asciimpi.MPI_Comm_rank(rank, 2, startwall, init_dt)
                dumpi.write(line + '\n')

                line, startwall = asciimpi.MPI_Comm_size(2, world_size, startwall, init_dt)
                dumpi.write(line + '\n')

                # write MPI sends
                for send in traffic[0]:
                    line, startwall = asciimpi.MPI_Send(startwall, dt, jobs[job_id]['size'], 1, send, 0, 2, startwall, dt, 0)
                    dumpi.write(line + '\n')

                # write MPI receives
                for recv in traffic[1]:
                    line, startwall = asciimpi.MPI_Recv(startwall, dt, jobs[job_id]['size'], 1, send, 0, 2, startwall, dt, 0)
                    dumpi.write(line + '\n')

                # write MPI Finalize stuff#####################################
                line, _ = asciimpi.MPI_Finalize(startwall, finalize_dt)
                dumpi.write(line)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Generate Dumpi Traces with parameters')
    parser.add_argument('config',    type=str,                help='file with list of job descriptions')
    parser.add_argument('output',    type=str,                help='output file name')
    parser.add_argument('-start',    type=float, default=100, help='trace wall start time (default 100)')
    parser.add_argument('-init_dt',  type=float, default=1,   help='time to run init functions (default 1)')
    parser.add_argument('-dt',       type=float, default=1,   help='time to run functions (default 1)')
    parser.add_argument('-final_dt', type=float, default=1,   help='time to run finalize functions (default 1)')
    args = parser.parse_args()

    generate_dumpi(simpleconfig.parse(args.config), args.output, args.start, args.init_dt, args.dt, args.final_dt)
