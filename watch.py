from psutil import process_iter
from psutil.error import NoSuchProcess, AccessDenied
from tracer import Tracer
from time import sleep
from signal import SIGSTOP, SIGCONT
from os import getuid, getpid

def watch(program_names, snapshots_per_second=1):
    interval = 1.0 / snapshots_per_second
    tracers = {}
    while not tracers:
        update_tracers(tracers, program_names)
        sleep(interval)
    while tracers:
        update_tracers(tracers, program_names)
        #pause(tracers)
        snapshots = take_snapshots(tracers)
        #resume(tracers)
        yield snapshots
        sleep(interval)

def update_tracers(tracers, program_names):
    existing = set(tracers.keys())
    running = set(p.pid for p in process_iter() if process_matches(p, program_names))
    forbidden = set(t.gdb.process.pid for t in tracers.itervalues()).union(set([getpid()]))
    running -= forbidden
    new = running - existing
    finished = existing - running

    for pid in finished:
        del tracers[pid]

    for pid in new:
        try:
            tracers[pid] = Tracer(pid)
        except (NoSuchProcess, AccessDenied):
            pass

def process_matches(p, program_names):
    try:
        return p.name in program_names and (getuid() == 0 or getuid() == p.uids[0])
    except (NoSuchProcess, AccessDenied):
        return False

def pause(tracers):
    for pid, t in tracers.iteritems():
        try:
            t.process.send_signal(SIGSTOP)
        except (NoSuchProcess, AccessDenied):
            pass

def resume(tracers):
    for pid, t in tracers.iteritems():
        try:
            t.process.send_signal(SIGCONT)
        except (NoSuchProcess, AccessDenied):
            pass

def take_snapshots(tracers):
    snapshots = []
    for t in tracers.itervalues():
        try:
            snapshots.append((t.about, t.snapshot()))
        except (NoSuchProcess, AccessDenied):
            pass
    return snapshots

if __name__ == '__main__':
    from sys import argv
    for snapshot in watch(set(argv[1:])):
        print snapshot
