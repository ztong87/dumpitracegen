# ###################################################################
#
# Traffic functions generate traffic for all ranks at the same time
#   Input:
#     start      = first rank
#     end        = last rank
#     n          = times to run generator before pulling output
#     iterations = number of communications from each rank
#
#   Output
#    {job id : {source rank: [destination ranks]}
#
# ###################################################################

# don't do from-import just in case there are name conflicts
import perm
import rand
import shift

# dictionary of traffic patterns to functions
patterns = {
    'perm'        : perm.perm,
    'permutation' : perm.perm,
    'shift'       : shift.shift,
    'rand'        : rand.rand,
    'random'      : rand.rand,
}

# returns {job id : {rank : [dst]}}
def generate_traffic(config):
    jobs = {}
    job_counter = 0
    for start, end, num_dst, size, iterations, pattern, count in config:
        # does not check for rank overlap
        jobs[job_counter] = patterns[pattern](start, end, count, iterations)
        job_counter += 1
    return jobs