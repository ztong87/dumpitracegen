# All to All Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat
def alltoall(job):
    return {src : (range(job['start'], src) + range(src + 1, job['end'] + 1)) * job['iterations'] for src in xrange(job['start'], job['end'] + 1)}
