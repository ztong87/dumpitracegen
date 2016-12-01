# read in configuration file
# formatted as lines of
#    rank-start rank-end number-of-destinations msg-size iterations pattern count
#
# ex:
#        0         255           3                1024       5       perm    1

# really simple parse
def parse_line(line):
    line = line.split()
    return [[int(field) for field in line[:5]] + [line[5], int(line[6])]]

def parse(filename):
    with open(filename, 'r') as config:
        jobs = []
        for line in config.readlines():
            parsed = parse_line(line)
            if len(parsed):
                jobs += parsed
        return jobs if len(jobs) else None
    return None