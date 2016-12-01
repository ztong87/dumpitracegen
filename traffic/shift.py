# shift right by n, with wrap around
def shift(start, end, n, iterations):
    traffic = {}
    for src in xrange(start, end + 1):
        dst = src + (n % (start - end + 1))
        if dst > end:
            dst -= start
        traffic[src] = [dst] * iterations
    return traffic
