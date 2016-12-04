# Random Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     skip       = number of random numbers to generate before pulling output
#     iterations = number of communications from each rank

import random

def rand(job):
    # helper function; generate 'skip' values before returning a random value
    def rng(start, end, src, skip):
        for _ in xrange(skip):
            random.randint(start, end)

        dst = random.randint(start, end)

        # keep generating until not talking to self
        while dst == src:
            dst = random.randint(start, end)

        return dst

    traffic = {}
    for src in xrange(job['start'], job['end'] + 1):
        traffic[src] = []
        for _ in xrange(job['iterations']):
            for _ in xrange(job['num_dst']):
                traffic[src] += [rng(job['start'],
                                     job['end'],
                                     src,
                                     job['skip'])]
    return traffic