import random

# generate n rounds before returning a random destination
def rand(start, end, n, iterations):
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
        traffic[src] = [rng(start, end, src, n) for _ in xrange(iterations)]
    return traffic