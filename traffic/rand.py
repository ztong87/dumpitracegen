# Random Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat
#     X          = number of communications from each rank

import random

def iteration(job):
    it = {src : [] for src in xrange(job['start'], job['end'] + 1)}
    for src in xrange(job['start'], job['end'] + 1):
        for _ in xrange(job['X']):
            dst = random.randint(job['start'], job['end'])
            while src == dst: # don't allow for src == dst, but allow for repeated dst
                dst = random.randint(job['start'], job['end'])
            it[src] += [dst]
    return it

def rand(job):
    traffic = {src : [] for src in xrange(job['start'], job['end'] + 1)}
    for _ in xrange(job['iterations']):
        for src, dsts in iteration(job).iteritems():
            traffic[src] += [dsts]
    return traffic
