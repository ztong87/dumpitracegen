# shuffle an array of ranks and take ranks i and i + 1 as SD pairs
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     skip       = number of pairs to skip before pulling output
#     iterations = number of communications from each rank

import random

def perm(job):
    possible_dst_count = job['end'] - job['start'] # does not include src

    # get num_dst destinations multiple times
    traffic = {rank : [] for rank in xrange(job['start'], job['end'] + 1)}
    for _ in xrange(job['iterations']):
        for src in xrange(job['start'], job['end'] + 1):
            # shuffled list of ranks not including source
            # do this across multiple iterations to get different permutations
            dst = range(job['start'], src) + range(src + 1, job['end'] + 1)
            random.shuffle(dst)

            # get num_dst destinations
            i = 0
            added = 0
            while added < job['num_dst']:
                i = ((i + job['skip'] * 2) % possible_dst_count)
                traffic[src] += [dst[i]];
                i += 2
                added += 1

    return traffic
