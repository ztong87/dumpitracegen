# ###################################################################
#
# Traffic functions generate traffic for all ranks at the same time
#   General Function Format:
#       def iteration(job):
#            ...
#            return {source rank: [destination ranks]}
#
#       def pattern_name(job):
#           traffic = {src : [] for src in xrange(job['start'], job['end'] + 1)}
#           for _ in xrange(job['iterations']):
#               for src, dst in iteration(job).iteritems():
#                   traffic[src] += [dst]
#           return traffic
#
#   Job:
#       A dictionary (str -> value) with all necessary fields to generate traffic
#
#   Traffic
#       {source rank: [[destination ranks for iteration i]]}
#
# ###################################################################

# don't do from-import just in case there are name conflicts
import alltoall
import DNN
import perm
import rand
import shift

# traffic patterns (and aliases) that can be used in config files
patterns = {
    'permutation'           : perm.perm,
    'shift_right'           : shift.shift_right,
    'shift_left'            : shift.shift_left,
    'random'                : rand.rand,
    'ring'                  : DNN.DNN,
    '2DNN'                  : DNN.DNN,
    '3DNN'                  : DNN.DNN,
    'DNN'                   : DNN.DNN,
    'pointtopoint_alltoall' : alltoall.pointtopoint_alltoall,
    'MPI_Alltoall'          : alltoall.MPI_Alltoall,
}

# any extra pattern specific data to extract
# if a pattern doesn't have data, it can return
# an empty array, or not even be in this dict
#
# Don't name any extra fields start, end, count, type, iterations, or pattern
pattern_specific = {
    'perm'                  : lambda line : {},
    'permutation'           : lambda line : {},
    'shift_right'           : lambda line : {'shift' : int(line[6]),},
    'shift_left'            : lambda line : {'shift' : int(line[6]),},
    'rand'                  : lambda line : {'X'     : int(line[6]),},
    'random'                : lambda line : {'X'     : int(line[6]),},
    'ring'                  : lambda line : {'dim'   : 1,},
    '2DNN'                  : lambda line : {'dim'   : 2,},
    '3DNN'                  : lambda line : {'dim'   : 3,},
    'DNN'                   : lambda line : {'dim'   : int(line[6]),},
    'pointtopoint_alltoall' : lambda line : {},
    'MPI_Alltoall'          : lambda line : {},
}