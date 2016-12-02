import named

def MPI_Initialized(startwall = 100, dt = 1):
    out  = 'MPI_Initialized entering at walltime {}, cputime {} seconds in thread 0.\n'.format(startwall, dt); startwall += dt
    out += 'int result=0\n'.format()
    out += 'MPI_Initialized returning at walltime {}, cputime {} seconds in thread 0.'.format(startwall, dt); startwall += dt
    return out, startwall

def MPI_Init(startwall, dt):
    out  = 'MPI_Init entering at walltime {}, cputime {} seconds in thread 0.\n'.format(startwall, dt); startwall += dt
    out += 'int argc=0\n'.format()
    out += 'string argv[0]=<IGNORED>\n'.format()
    out += 'MPI_Init returning at walltime {}, cputime {} seconds in thread 0.'.format(startwall, dt); startwall += dt
    return out, startwall

def MPI_Comm_rank(rank, comm, startwall, dt):
    out  = 'MPI_Comm_rank entering at walltime {}, cputime {} seconds in thread 0.\n'.format(startwall, dt); startwall += dt
    out += 'MPI_Comm comm={} ({})\n'.format(comm, named.comm[comm])
    out += 'int rank={}\n'.format(rank)
    out += 'MPI_Comm_rank returning at walltime {}, cputime {} seconds in thread 0.'.format(startwall, dt); startwall += dt
    return out, startwall

def MPI_Comm_size(comm, world_size, startwall, dt):
    out  = 'MPI_Comm_size entering at walltime {}, cputime {} seconds in thread 0.\n'.format(startwall, dt); startwall += dt
    out += 'MPI_Comm comm={} ({})\n'.format(comm, named.comm[comm])
    out += 'int size={}\n'.format(world_size)
    out += 'MPI_Comm_size returning at walltime {}, cputime {} seconds in thread 0.'.format(startwall, dt); startwall += dt
    return out, startwall + dt

def MPI_Finalize(end, final_dt):
    out  = "MPI_Finalize entering at walltime {}, cputime {} seconds in thread 0.\n".format(end, final_dt); end += final_dt
    out += "MPI_Finalize returning at walltime {}, cputime {} seconds in thread 0.".format(end, final_dt);
    return out, None

def MPI_Send(startwall, startcpu, count, type, dst, tag, comm, endwall, endcpu, thread = 0):
    return '\n'.join([
                        'MPI_Send entering at walltime {}, cputime {} seconds in thread {}.'.format(startwall, startcpu, thread),
                        'int count={}'.format(count),
                        'MPI_Datatype datatype={} ({})'.format(type, named.val2type[type]),
                        'int dest={}'.format(dst),
                        'int tag={}'.format(tag),
                        'MPI_Comm comm={} ({})'.format(comm, named.comm[comm]),
                        'MPI_Send returning at walltime {}, cputime {} seconds in thread {}.'.format(endwall, endcpu, thread)
                     ]), endwall + endcpu

def MPI_Recv(startwall, startcpu, count, type, dst, tag, comm, endwall, endcpu, thread = 0):
    return '\n'.join([
                        'MPI_Recv entering at walltime {}, cputime {} seconds in thread {}.'.format(startwall, startcpu, thread),
                        'int count={}'.format(count),
                        'MPI_Datatype datatype={} ({})'.format(type, named.val2type[type]),
                        'int dest={}'.format(dst),
                        'int tag={}'.format(tag),
                        'MPI_Comm comm={} ({})'.format(comm, named.comm[comm]),
                        'MPI_Status status=<IGNORED>',
                        'MPI_Recv returning at walltime {}, cputime {} seconds in thread {}.'.format(endwall, endcpu, thread)
                    ]), endwall + endcpu
