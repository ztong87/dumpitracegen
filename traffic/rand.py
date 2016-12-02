import random

# generate n rounds before returning a random destination
def rand(start, end, n, num_dst, iterations):
    # helper function
    def rng(start, end, src, n):
        for _ in xrange(n):
            random.randint(start, end)

        dst = random.randint(start, end)

        # keep generating until not talking to self
        while dst == src:
            dst = random.randint(start, end)

        return dst

    traffic = {}
    for src in xrange(start, end + 1):
        traffic[src] = []
        for _ in xrange(iterations):
            for _ in xrange(num_dst):
                traffic[src] += [rng(start, end, src, n)]
    return traffic