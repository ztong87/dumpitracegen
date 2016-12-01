import itertools

# generate all combinations; skip n indicies; get sd pair
# this is wrong
def perm(start, end, n, iterations):
    traffic = {rank : [] for rank in xrange(start, end + 1)}
    perms   = {rank : [] for rank in xrange(start, end + 1)}

    total_iterations = iterations * (end - start + 1)
    while total_iterations > 0:
        for src in xrange(start, end + 1):
            while not len(perms[src]):
                # generate more values
                for s, d in itertools.combinations(xrange(start, end), 2):
                    perms[s] += [d]

            if len(perms[src]) > n:
                if len(traffic[src]) < iterations:
                    traffic[src] += [perms[src][n]]  # read nth value
                    perms[src] = perms[src][n + 1:]  # 'pop front'
                    total_iterations -= 1
    return traffic
