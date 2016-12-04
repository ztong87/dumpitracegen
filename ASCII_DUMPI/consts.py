# https://github.com/sstsimulator/sst-dumpi/blob/1d1ef777668b2982efed862c4275cc1341225623/dumpi/common/constants.h

num_datatype = {
    2  : 'MPI_CHAR',
    3  : 'MPI_SIGNED_CHAR',
    4  : 'MPI_UNSIGNED_CHAR',
    5  : 'MPI_BYTE',
    6  : 'MPI_WCHAR',
    7  : 'MPI_SHORT',
    8  : 'MPI_UNSIGNED_SHORT',
    9  : 'MPI_INT',
    10 : 'MPI_UNSIGNED',
    11 : 'MPI_LONG',
    12 : 'MPI_UNSIGNED_LONG',
    13 : 'MPI_FLOAT',
    14 : 'MPI_DOUBLE',
    15 : 'MPI_LONG_DOUBLE',
    16 : 'MPI_LONG_LONG_INT',
    17 : 'MPI_UNSIGNED_LONG_LONG',
    18 : 'MPI_LONG_LONG',
    19 : 'MPI_PACKED',
    20 : 'MPI_LB',
    21 : 'MPI_UB',
    22 : 'MPI_FLOAT_INT',
    23 : 'MPI_DOUBLE_INT',
    24 : 'MPI_LONG_INT',
    25 : 'MPI_SHORT_INT',
    26 : 'MPI_2INT',
    27 : 'MPI_LONG_DOUBLE_INT',
}

# inverse of num_datatypes
str_datatype = {val : key for key, val in num_datatype.iteritems()}

# communicators
num_communicator = {
    2 : 'MPI_COMM_WORLD',
    3 : 'MPI_COMM_SELF',
}