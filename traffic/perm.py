# Permutation Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat

import random

def iteration(job):
    traffic = {src : [] for src in xrange(job['start'], job['end'] + 1)}

    # shuffled list of ranks
    pairs = range(job['start'], job['end'] + 1)
    random.shuffle(pairs)

    # wrap around
    pairs += [pairs[0]]

    # pairs[i] -> pairs[i + 1] for all i
    return {pairs[i] : [pairs[i + 1]] for i in xrange(len(pairs) - 1)}

def perm(job):
    traffic = {src : [[]] for src in xrange(job['start'], job['end'] + 1)}
    for _ in xrange(job['iterations']):
        for src, dst in iteration(job).iteritems():
            traffic[src] += [dst]
    return traffic
