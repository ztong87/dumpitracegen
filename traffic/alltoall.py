# Point to Point All to All Traffic Pattern
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     iterations = number of times to repeat
def pointtopoint_alltoall(job):
    return {src : [(range(job['start'], src) + range(src + 1, job['end'] + 1))] * job['iterations'] for src in xrange(job['start'], job['end'] + 1)}

# special case; do not call from traffic.patterns
def MPI_Alltoall(job):
    return {src : [] for src in xrange(job['start'], job['end'] + 1)}
