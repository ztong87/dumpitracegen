# parse methods
import simple

# other imports
import traffic

# avaliable parsers
# all parsers parse individual lines
parsers = {
    'simple' : simple.parse,
}

# Takes in a filename string, reads each formatted line
# and returns an array of jobs with their descriptions
# [{field : value}]
def parse(filename):
    jobs = []
    with open(filename, 'r') as config:
        # get rid of empty lines and comment lines
        lines = []
        for line in config.readlines():
            line.strip()
            if (len(line) == 0) or (line == '\n') or (line[0] == '#'):
                continue
            lines += [line]

        # first line must be parser name
        parser_name = lines[0][:-1]
        if parser_name not in parsers:
            return jobs
        parser = parsers[parser_name]

        # parse rest of lines
        for line in lines[1:]:
            jobs += [parser(line)]

    return jobs

# Generate traffic for one job
# returns {rank : [dst]}
def generate_traffic(job):
    return traffic.patterns[job['pattern']](job)
