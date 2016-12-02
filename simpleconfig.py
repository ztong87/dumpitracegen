import traffic

# Takes in a formatted line of the format
# rank-start rank-end number-of-destinations msg-size (bytes) iterations pattern count
# ex:
#    0         255           3                   1024              5      rand     1

# and returns of dictionary of these values: {field : value}
def parse_line(line):
    line = line.split()
    return {
            'start'       : int(line[0]),
            'end'         : int(line[1]),
            'num_dst'     : int(line[2]),
            'size'        : int(line[3]),
            'iterations'  : int(line[4]),
            'pattern'     :     line[5],
            'count'       : int(line[6]),
           }

# Takes in a string, opens it, and returns a
# dictionary of results from parse_line
# {job id : {field : value}}
def parse(filename):
    jobs = {}
    with open(filename, 'r') as config:
        job_counter = 0
        for line in config.readlines():
            parsed = parse_line(line)
            if parsed:
                jobs[job_counter] = parsed
                job_counter += 1
    return jobs

# Generate Traffic based on the given jobs from parse
# returns {job id : {rank : [dst]}}
# Note: Does not check for rank overlap
def generate_traffic(config):
    jobs = {}
    for index, values in config.iteritems():
        jobs[index] = traffic.patterns[values['pattern']](values['start'],
                                                          values['end'],
                                                          values['count'],
                                                          values['num_dst'],
                                                          values['iterations'])
    return jobs