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
import perm
import rand
import shift

# traffic patterns that can be used in config files
patterns = {
    'perm'        : perm.perm,
    'permutation' : perm.perm,
    'shift'       : shift.shift,
    'rand'        : rand.rand,
    'random'      : rand.rand,
}
