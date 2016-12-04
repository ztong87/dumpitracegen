# Simple configuration line parser
#
# Takes in a formatted line of the format
# rank-start rank-end number-of-destinations msg-count msg-type  iterations pattern pattern-specific
# ex:
#     0         255           3                1024    MPI_CHAR       5      rand          1
#
# and returns of dictionary of these values: {field : value}
def parse(line):
    line = line.split()

    # allow for empty lines and comment lines
    if (len(line) == 0) or (line[0] == '#'):
       return None

    # common fields
    out = {
           'start'       : int(line[0]),
           'end'         : int(line[1]),
           'num_dst'     : int(line[2]),
           'count'       : int(line[3]),
           'type'        :     line[4],
           'iterations'  : int(line[5]),
           'pattern'     :     line[6],
          }

    if (out['pattern'] == 'rand') or (out['pattern'] == 'random'):
        out['skip'] = int(line[7])
    elif (out['pattern'] == 'perm') or (out['pattern'] == 'permutation'):
        out['skip'] = int(line[7])
    elif out['pattern'] == 'shift':
        out['shift'] = int(line[7])
    else:
        return None
    return out

