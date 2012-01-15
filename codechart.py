# Copyright 2011, 2012 Mark O'Connor. This program is distributed under the terms of the GNU General Public License v3.

from collections import defaultdict
from watch import watch
from json import dump, dumps
from optparse import OptionParser
from sys import exit
from output import format_output

def main():
    parser = OptionParser()
    options, args = parser.parse_args()
    if not args:
        parser.print_usage()
        exit(1)
    output_name = args[0]
    watch_and_log(args, output_name)

def watch_and_log(program_names, output_name, capture_rate=2):
    results = defaultdict(list)
    for iteration, snapshots in enumerate(watch(set(program_names), capture_rate)):
        for key, value in snapshots:
            results[key].append((iteration, value))

        if iteration % (capture_rate * 10) == 0:
            write_log(results, output_name)
    write_log(results, output_name)

def write_log(results, output_name):
    output = [ { 'i': i, 'name': name, 'pid': pid, 'start_time': start_time.isoformat(), 'data': data } for i, ((name, pid, start_time), data) in enumerate(sorted(results.iteritems(), key=lambda k:k[0][2])) if len(data) > 1 ] # a list of entries sorted by ascending start time
    json, html = format_output(output)
    open(output_name + '.json', 'w').write(json)
    open(output_name + '.html', 'w').write(html)
    print 'Written %s.json and %s.html' % (output_name, output_name)

if __name__ == '__main__':
    main()
