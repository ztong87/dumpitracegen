# ###################################################################
#
# Traffic functions generate traffic for all ranks at the same time
#   Input:
#       A dictionary (str -> value) with all necessary fields to generate traffic
#
#   Output
#       {source rank: [destination ranks]}
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
    'perm'        : perm.perm,
    'permutation' : perm.perm,
    'shift_right' : shift.shift_right,
    'shift_left'  : shift.shift_left,
    'rand'        : rand.rand,
    'random'      : rand.rand,
    'DNN'         : DNN.DNN,
    'ring'        : DNN.DNN,
    '2DNN'        : DNN.DNN,
    '2dnn'        : DNN.DNN,
    '3DNN'        : DNN.DNN,
    '3dnn'        : DNN.DNN,
    'alltoall'    : alltoall.alltoall,
    'all2all'     : alltoall.alltoall,
}

# any extra pattern specific data to extract
# if a pattern doesn't have data, it can return
# an empty array, or not even be in this dict
pattern_specific = {
    'perm'        : lambda line : {},
    'permutation' : lambda line : {},
    'shift_right' : lambda line : {'shift' : int(line[6]),},
    'shift_left'  : lambda line : {'shift' : int(line[6]),},
    'rand'        : lambda line : {'count' : int(line[6]),},
    'random'      : lambda line : {'count' : int(line[6]),},
    'DNN'         : lambda line : {'dim'   : int(line[6]),},
    'ring'        : lambda line : {'dim'   : 1,},
    '2DNN'        : lambda line : {'dim'   : 2,},
    '2dnn'        : lambda line : {'dim'   : 2,},
    '3DNN'        : lambda line : {'dim'   : 3,},
    '3dnn'        : lambda line : {'dim'   : 3,},
    'alltoall'    : lambda line : {},
    'all2all'     : lambda line : {},
}