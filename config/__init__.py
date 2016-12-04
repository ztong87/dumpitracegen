# parse methods
import simple

# other imports
import traffic

# known line parsers
parsers = {
    'simple' : simple.parse,
}

# Takes in a filename string, reads each line and returns a
# dictionary of results from parse_line
# {job id : {field : value}}
def parse(filename, line_parser):
    jobs = {}
    with open(filename, 'r') as config:
        job_counter = 0
        for line in config.readlines():
            parsed = line_parser(line)
            if parsed:
                jobs[job_counter] = parsed
                job_counter += 1
    return jobs

# Generate Traffic based on the given jobs from parse
# returns {job id : {rank : [dst]}}
# Note: Does not check for rank overlap
def generate_traffic(config):
    jobs = {}
    for index, job in config.iteritems():
        jobs[index] = traffic.patterns[job['pattern']](job)
    return jobs
