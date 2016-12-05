# Permutation Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat

import random

def perm(job):
    traffic = {rank : [] for rank in xrange(job['start'], job['end'] + 1)}

    for _ in xrange(job['iterations']):
        # shuffled list of ranks
        pairs = range(job['start'], job['end'] + 1)
        random.shuffle(pairs)

        # pairs[i] -> pairs[i + 1]
        for i in xrange(0, len(pairs), 2):
            traffic[pairs[i]] += [pairs[i + 1]]

    return traffic
