# shift right by n, with wrap around
def shift(start, end, n, num_dst, iterations):
    traffic = {}
    for src in xrange(start, end + 1):
        dst = src + (n % (end - start + 1))
        if dst > end:
            dst -= end - start
        traffic[src] = [dst] * num_dst * iterations
    return traffic
