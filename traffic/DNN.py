# N Dimensional Nearest Neighbor
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat
#     dim        = dimensions

import copy
import math
import shift

# copied from traceReader
def DNN(job):
    traffic = {rank : [] for rank in xrange(job['start'], job['end'] + 1)}

    # number of ranks
    count = job['end'] - job['start'] + 1

    # number of elements per dimension
    d_size = int(math.ceil(count ** (1. / job['dim'])))

    # calculate offsets
    Ds = [1]
    for i in xrange(job['dim']):
        Ds += [Ds[i - 1] * d_size];

    # figure out who each node is talking to
    for nid in xrange(count):
        # First, find the logical coordinates for the current node
        remainder = nid
        Dims = [0] * job['dim']
        for i in xrange(job['dim'] - 1, -1, -1):
            Dims[i] = remainder / Ds[i]
            remainder %= Ds[i]

        # find its neighbors
        for i in xrange(job['dim']):
            # refresh source coordinates
            neighbor = copy.copy(Dims)

            # +1 in dimension, with wrap around
            neighbor[i] = (Dims[i] + 1) % d_size
            dst_id = 0

            # recombine coordinates into one
            for j in xrange(job['dim']):
                dst_id += neighbor[j] * Ds[j]

            # if neighbor is too large, remove the dimension
            if dst_id >= count:
               dst_id -= neighbor[i] * Ds[i]

            if nid != dst_id:
              # add to set of traffic
              traffic[job['start'] + nid] += [job['start'] + dst_id]

            # -1 in dimension with wrap around
            neighbor[i] = (Dims[i] + d_size - 1) % d_size
            dst_id = 0

            # recombine coordinates into one
            for j in xrange(job['dim']):
                dst_id += neighbor[j] * Ds[j]

            # remove from dimension until coordinate is valid node again
            while dst_id >= count:
                dst_id -= Ds[i]

            if nid != dst_id:
              # add to set of traffic
              traffic[job['start'] + nid] += [job['start'] + dst_id]

    return traffic
