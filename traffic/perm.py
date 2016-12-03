import random

# generate all combinations; skip n indicies; get sd pair
def perm(start, end, n, num_dst, iterations):
    possible_dst_count = end - start # does not include src

    # get num_dst destinations multiple times
    traffic = {rank : [] for rank in xrange(start, end + 1)}
    for aaa in xrange(iterations):
        for src in xrange(start, end + 1):
            # shuffled list of ranks not including source
            # do this across multiple iterations to get different permutations
            dst = range(start, src) + range(src + 1, end + 1)
            random.shuffle(dst)

            # get num_dst destinations
            i = 0
            added = 0
            while added < num_dst:
                i = ((i + n) % possible_dst_count)
                traffic[src] += [dst[i]];
                i += 1
                added += 1

    return traffic
