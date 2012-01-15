# Copyright 2011, 2012 Mark O'Connor. This program is distributed under the terms of the GNU General Public License v3.

from traceback import format_stack
from signal import signal, SIGPROF
from json import dump
from os import getpid, rename

def log_stack(sig, frame):
    lines = format_stack()[:-1]
    filename = '/tmp/%d.stack' % getpid()
    f = open(filename + '~', 'w')
    dump(lines, f)
    f.close()
    rename(filename + '~', filename)

signal(SIGPROF, log_stack)  # Register handler

if __name__ == '__main__':
    def a():
        while True:
            pass
    print getpid()
    a()
