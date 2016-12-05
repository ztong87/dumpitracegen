# Random Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat
#     count      = number of communications from each rank

import random

def rand(job):
    traffic = {}
    for src in xrange(job['start'], job['end'] + 1):
        traffic[src] = []
        for _ in xrange(job['iterations']):
            for _ in xrange(job['count']):
                dst = random.randint(job['start'], job['end'])
                while src == dst: # don't allow for src == dst, but allow for repeated dst
                    dst = random.randint(job['start'], job['end'])
                traffic[src] += [dst]
    return traffic