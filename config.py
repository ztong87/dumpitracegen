# Configuration Line Parser
#
# Takes in a formatted line of the format
# rank-start rank-end msg-count msg-type  iterations pattern pattern-specific-values
# ex:
#     0         255     1024    MPI_CHAR       5      rand               1
#
# and returns of dictionary of these values: {field : value}, or None if it got a comment/empty line
#
# Available values for traffic patterns can be found in traffic/__init__.py.
# Job ranks are contiguous.
#

import traffic

# parse a single line
def parse_line(line):
    line = line.split()

    # common fields
    out = {
           'start'       : int(line[0]),
           'end'         : int(line[1]),
           'count'       : int(line[2]),
           'type'        :     line[3],
           'iterations'  : int(line[4]),
           'pattern'     :     line[5],
          }

    # read in pattern specific values
    out.update(traffic.pattern_specific[out['pattern']](line))
    return out

# Takes in a filename string, reads each formatted line
# and returns an array of jobs with their descriptions
# [{field : value}]
def parse(filename):
    jobs = []
    with open(filename, 'r') as config:
        # get rid of empty lines and comment lines
        lines = []
        for line in config.readlines():
            line.strip()
            if (len(line) == 0) or (line == '\n') or (line[0] == '#'):
                continue
            lines += [line]

        # parse rest of lines
        for line in lines:
            jobs += [parse_line(line)]

    return jobs

# Generate traffic for one job
# returns {rank : [[dst]]}
def generate_traffic(job):
    return traffic.patterns[job['pattern']](job)
