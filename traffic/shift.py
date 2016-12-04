# shift right with wrap around
#   Input Fields:
#     start      = first rank
#     end        = last rank
#     shift      = number of indicies to shift by
#     iterations = number of communications from each rank

def shift(job):
    traffic = {}

    # don't recalculate this
    repetitions = job['num_dst'] * job['iterations']

    for src in xrange(job['start'], job['end'] + 1):
        dst = src + (job['shift'] % (job['end'] - job['start'] + 1))
        if dst > job['end']:
            dst -= job['end'] - job['start']
        traffic[src] = [dst] * repetitions
    return traffic
