# Taken from https://github.com/sstsimulator/sst-macro/blob/d360f1fcb8dbcee0b70a33e3c6498fc6a17333f8/sumi-mpi/sstmac_mpi_integers.h
# but somehow still incorrect

num_datatype = {
    0 : 'MPI_NULL',
    1 : 'MPI_CHAR',
    2 : 'MPI_BYTE',
    3 : 'MPI_SHORT',
    4 : 'MPI_INT',
    5 : 'MPI_LONG',
    6 : 'MPI_FLOAT',
    7 : 'MPI_DOUBLE',
    8 : 'MPI_UNSIGNED_CHAR',
    9 : 'MPI_UNSIGNED_SHORT',
    10 : 'MPI_UNSIGNED',
    11 : 'MPI_UNSIGNED_LONG',
    12 : 'MPI_LONG_DOUBLE',
    13 : 'MPI_LONG_LONG_INT',
    14 : 'MPI_PACKED',
    15 : 'MPI_UB',
    16 : 'MPI_LB',
    17 : 'MPI_DOUBLE_INT',
    18 : 'MPI_2INT',
    19 : 'MPI_LONG_INT',
    20 : 'MPI_FLOAT_INT',
    21 : 'MPI_SHORT_INT',
    22 : 'MPI_LONG_DOUBLE_INT',
    23 : 'MPI_SIGNED_CHAR',
    24 : 'MPI_WCHAR',
    25 : 'MPI_UNSIGNED_LONG_LONG',
    26 : 'MPI_COMPLEX',
    27 : 'MPI_DOUBLE_COMPLEX',
    28 : 'MPI_LOGICAL',
    29 : 'MPI_REAL',
    30 : 'MPI_DOUBLE_PRECISION',
    31 : 'MPI_INTEGER',
    32 : 'MPI_2INTEGER',
    33 : 'MPI_2REAL',
    34 : 'MPI_2DOUBLE_PRECISION',
    35 : 'MPI_CHARACTER',
    36 : 'MPI_INT8_T',
    37 : 'MPI_INT16_T',
    38 : 'MPI_INT32_T',
    39 : 'MPI_INT64_T',
    40 : 'MPI_UINT8_T',
    41 : 'MPI_UINT16_T',
    42 : 'MPI_UINT32_T',
    43 : 'MPI_UINT64_T',
    44 : 'MPI_REAL4',
    45 : 'MPI_REAL8',
    46 : 'MPI_REAL16',
    47 : 'MPI_COMPLEX8',
    48 : 'MPI_COMPLEX16',
    49 : 'MPI_INTEGER1',
    50 : 'MPI_INTEGER2',
    51 : 'MPI_INTEGER4',
    52 : 'MPI_INTEGER8'
}

# inverse of num_datatypes
str_datatype = {val : key for key, val in num_datatype.iteritems()}

# communicators
num_communicator = {
    2          : 'MPI_COMM_WORLD',
}