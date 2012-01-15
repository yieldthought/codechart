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
